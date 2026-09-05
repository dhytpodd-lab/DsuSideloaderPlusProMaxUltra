package yangfentuozi.dsusideloaderplus.util

import android.util.Log
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.ExecutionException
import java.util.concurrent.ExecutorCompletionService
import java.util.concurrent.Executors

object GitHubRequestUtil {
    private const val TAG = "GitHubRequestUtil"

    data class RaceResult<C, T>(
        val candidate: C,
        val value: T,
    )

    data class TextResult(
        val body: String,
        val proxyBaseUrl: String?,
    )

    private data class RequestCandidate(
        val url: String,
        val proxyBaseUrl: String?,
        val githubResource: Boolean = false,
    )

    private data class GithubRoute(
        val proxyBaseUrl: String?,
    )

    private const val MAX_PROXY_ATTEMPTS = 8
    private const val DEFAULT_CONNECT_TIMEOUT_MS = 10_000
    private const val DEFAULT_READ_TIMEOUT_MS = 10_000
    private const val PROXY_LIST_TIMEOUT_MS = 3_000
    private const val GITHUB_PROXY_LIST_URL =
        "https://cdn.jsdelivr.net/gh/Itosang/GitHub-Proxy@main/websites"
    private const val RAW_GITHUB_USER_CONTENT_BASE_URL =
        "https://raw.githubusercontent.com/"
    private const val JSDELIVR_GITHUB_BASE_URL =
        "https://cdn.jsdelivr.net/gh"
    private const val FASTLY_JSDELIVR_GITHUB_BASE_URL =
        "https://fastly.jsdelivr.net/gh"

    private val fallbackProxyBaseUrls = listOf(
        "https://ghfast.top/",
        "https://gh-proxy.org/",
        "https://ghproxy.vip/",
        "https://ghproxy.net/",
        "https://gh-proxy.com/",
        "https://ghproxy.imciel.com/",
        "https://gh.idayer.com/",
        "https://gh.monlor.com/",
        "https://g.blfrp.cn/",
        "https://ghp.keleyaa.com/",
        "https://gh.qninq.cn/",
        "https://gitproxy.mrhjx.cn/",
        "https://gh.noki.icu/",
        "https://gh.catmak.name/",
        "https://github.xxlab.tech/",
        "https://ghp.arslantu.xyz/",
        "https://github.ednovas.xyz/",
        "https://git.669966.xyz/",
        "https://gh.jasonzeng.dev/",
        "https://gh.nxnow.top/",
        "https://gh.noki.eu.org/",
        "https://tvv.tw/",
    )

    @Volatile
    private var cachedProxyBaseUrls: List<String>? = null

    @Volatile
    private var preferredGithubRoute: GithubRoute? = null

    fun <C, T> firstSuccessful(
        candidates: List<C>,
        description: String,
        candidateLabel: (C) -> String = { it.toString() },
        request: (C) -> T,
    ): RaceResult<C, T> {
        if (candidates.isEmpty()) {
            throw IllegalStateException("No request candidates, description=$description")
        }

        val executor = Executors.newFixedThreadPool(candidates.size)
        val completionService = ExecutorCompletionService<RaceResult<C, T>>(executor)
        val futures = candidates.map { candidate ->
            completionService.submit {
                Log.v(TAG, "Race request started, description=$description candidate=${candidateLabel(candidate)}")
                RaceResult(
                    candidate = candidate,
                    value = request(candidate),
                )
            }
        }

        var lastError: Exception? = null
        try {
            repeat(futures.size) {
                try {
                    return completionService.take().get()
                } catch (error: InterruptedException) {
                    Thread.currentThread().interrupt()
                    throw error
                } catch (error: ExecutionException) {
                    val cause = error.cause
                    lastError = cause as? Exception
                        ?: RuntimeException("Race request failed, description=$description", cause)
                    Log.w(TAG, "Race request failed, description=$description", lastError)
                }
            }
        } finally {
            futures.forEach { it.cancel(true) }
            executor.shutdownNow()
        }

        throw lastError ?: IllegalStateException("All request candidates failed, description=$description")
    }

    fun requestText(
        resourceUrl: String,
        description: String,
        preferredProxyBaseUrl: String? = null,
    ): TextResult {
        if (!isGithubResourceUrl(resourceUrl)) {
            return TextResult(
                body = requestResponseBody(resourceUrl),
                proxyBaseUrl = null,
            )
        }

        getPreferredGithubRoute(preferredProxyBaseUrl)?.let { route ->
            try {
                return requestFirstSuccessful(
                    candidates = listOf(buildGithubResourceCandidate(resourceUrl, route)),
                    description = "Preferred GitHub route $description",
                )
            } catch (error: Exception) {
                clearPreferredGithubRoute(route, error)
            }
        }

        return requestFirstSuccessful(
            candidates = buildGithubResourceCandidates(resourceUrl, preferredProxyBaseUrl),
            description = "GitHub raw/proxy $description",
        )
    }

    fun requestTextWithJsDelivrFallback(
        resourceUrl: String,
        description: String,
        preferredProxyBaseUrl: String? = null,
    ): TextResult {
        if (!isGithubResourceUrl(resourceUrl)) {
            return TextResult(
                body = requestResponseBody(resourceUrl),
                proxyBaseUrl = null,
            )
        }

        var lastError: Exception?
        try {
            return requestText(
                resourceUrl = resourceUrl,
                description = description,
                preferredProxyBaseUrl = preferredProxyBaseUrl,
            )
        } catch (error: Exception) {
            lastError = error
            Log.w(
                TAG,
                "All GitHub raw/proxy requests failed, trying jsDelivr, description=$description",
                error,
            )
        }

        val jsDelivrUrls = buildJsDelivrUrls(resourceUrl)
        if (jsDelivrUrls.isNotEmpty()) {
            try {
                val result = firstSuccessful(
                    candidates = jsDelivrUrls,
                    description = "jsDelivr $description",
                    candidateLabel = { it },
                ) { url ->
                    requestResponseBody(url)
                }
                return TextResult(
                    body = result.value,
                    proxyBaseUrl = null,
                )
            } catch (error: Exception) {
                lastError = error
            }
        }

        throw lastError
    }

    fun routeGithubUrl(url: String, proxyBaseUrl: String?): String {
        if (url.isBlank() || proxyBaseUrl.isNullOrBlank()) return url
        if (!isGithubResourceUrl(url)) return url
        return buildProxyUrl(proxyBaseUrl, url)
    }

    private fun requestFirstSuccessful(
        candidates: List<RequestCandidate>,
        description: String,
    ): TextResult {
        val result = firstSuccessful(
            candidates = candidates,
            description = description,
            candidateLabel = { it.url },
        ) { candidate ->
            requestResponseBody(candidate.url)
        }
        rememberPreferredGithubRoute(result.candidate)
        return TextResult(
            body = result.value,
            proxyBaseUrl = result.candidate.proxyBaseUrl,
        )
    }

    private fun buildGithubResourceCandidates(
        resourceUrl: String,
        preferredProxyBaseUrl: String?,
    ): List<RequestCandidate> {
        val preferredRoute = getPreferredGithubRoute(preferredProxyBaseUrl)
        val allRoutes = listOf(GithubRoute(proxyBaseUrl = null)) +
            getOrderedProxyBaseUrls(preferredProxyBaseUrl).map { GithubRoute(proxyBaseUrl = it) }
        val orderedRoutes = if (preferredRoute == null) {
            allRoutes
        } else {
            listOf(preferredRoute) + allRoutes.filterNot { it == preferredRoute }
        }
        return orderedRoutes
            .distinct()
            .map { buildGithubResourceCandidate(resourceUrl, it) }
    }

    private fun buildGithubResourceCandidate(
        resourceUrl: String,
        route: GithubRoute,
    ): RequestCandidate {
        val proxyBaseUrl = route.proxyBaseUrl
        return RequestCandidate(
            url = if (proxyBaseUrl.isNullOrBlank()) {
                resourceUrl
            } else {
                buildProxyUrl(proxyBaseUrl, resourceUrl)
            },
            proxyBaseUrl = proxyBaseUrl,
            githubResource = true,
        )
    }

    private fun getPreferredGithubRoute(preferredProxyBaseUrl: String?): GithubRoute? =
        preferredGithubRoute ?: preferredProxyBaseUrl?.let { GithubRoute(proxyBaseUrl = it) }

    private fun rememberPreferredGithubRoute(candidate: RequestCandidate) {
        if (!candidate.githubResource) return
        val route = GithubRoute(proxyBaseUrl = candidate.proxyBaseUrl)
        preferredGithubRoute = route
        Log.d(TAG, "Remembered available GitHub route: ${route.displayName()}")
    }

    private fun clearPreferredGithubRoute(route: GithubRoute, error: Exception) {
        if (preferredGithubRoute == route) {
            preferredGithubRoute = null
        }
        Log.w(TAG, "Preferred GitHub route failed: ${route.displayName()}", error)
    }

    private fun GithubRoute.displayName(): String =
        proxyBaseUrl ?: "raw.githubusercontent.com"

    private fun getOrderedProxyBaseUrls(preferredProxyBaseUrl: String?): List<String> {
        val proxyBaseUrls = loadProxyBaseUrls()
        val orderedProxyBaseUrls = if (preferredProxyBaseUrl.isNullOrBlank()) {
            proxyBaseUrls
        } else {
            listOf(preferredProxyBaseUrl) + proxyBaseUrls.filterNot { it == preferredProxyBaseUrl }
        }
        return orderedProxyBaseUrls.take(MAX_PROXY_ATTEMPTS)
    }

    private fun loadProxyBaseUrls(): List<String> {
        cachedProxyBaseUrls?.let { return it }
        return try {
            val proxies = requestResponseBody(
                url = GITHUB_PROXY_LIST_URL,
                connectTimeoutMs = PROXY_LIST_TIMEOUT_MS,
                readTimeoutMs = PROXY_LIST_TIMEOUT_MS,
            )
                .lineSequence()
                .map { it.trim() }
                .filter { it.startsWith("https://") }
                .map { if (it.endsWith("/")) it else "$it/" }
                .distinct()
                .toList()
                .ifEmpty { fallbackProxyBaseUrls }
            cachedProxyBaseUrls = proxies
            proxies
        } catch (error: Exception) {
            Log.w(TAG, "Failed to load proxy list, using bundled fallback list", error)
            fallbackProxyBaseUrls
        }
    }

    private fun buildProxyUrl(proxyBaseUrl: String, resourceUrl: String): String {
        val base = if (proxyBaseUrl.endsWith("/")) proxyBaseUrl else "$proxyBaseUrl/"
        return base + resourceUrl
    }

    private fun isGithubResourceUrl(url: String): Boolean =
        url.startsWith("https://github.com/") ||
            url.startsWith(RAW_GITHUB_USER_CONTENT_BASE_URL) ||
            url.startsWith("https://objects.githubusercontent.com/") ||
            url.startsWith("https://release-assets.githubusercontent.com/")

    private fun buildJsDelivrUrls(resourceUrl: String): List<String> {
        if (!resourceUrl.startsWith(RAW_GITHUB_USER_CONTENT_BASE_URL)) return emptyList()
        val rawPath = resourceUrl.removePrefix(RAW_GITHUB_USER_CONTENT_BASE_URL)
        val parts = rawPath.split("/", limit = 4)
        if (parts.size < 4) return emptyList()

        val owner = parts[0]
        val repository = parts[1]
        val branch = parts[2]
        val path = parts[3]
        if (owner.isBlank() || repository.isBlank() || branch.isBlank() || path.isBlank()) {
            return emptyList()
        }

        val jsDelivrPath = "$owner/$repository@$branch/$path"
        return listOf(
            "$JSDELIVR_GITHUB_BASE_URL/$jsDelivrPath",
            "$FASTLY_JSDELIVR_GITHUB_BASE_URL/$jsDelivrPath",
        )
    }

    private fun requestResponseBody(
        url: String,
        connectTimeoutMs: Int = DEFAULT_CONNECT_TIMEOUT_MS,
        readTimeoutMs: Int = DEFAULT_READ_TIMEOUT_MS,
    ): String {
        var connection: HttpURLConnection? = null
        try {
            connection = openConnection(url, connectTimeoutMs, readTimeoutMs)
            val responseCode = connection.responseCode
            if (responseCode != HttpURLConnection.HTTP_OK) {
                error("Request failed, responseCode=$responseCode url=$url")
            }
            return connection.inputStream.bufferedReader().use { it.readText() }
        } finally {
            connection?.disconnect()
        }
    }

    private fun openConnection(
        url: String,
        connectTimeoutMs: Int,
        readTimeoutMs: Int,
    ): HttpURLConnection =
        (URL(url).openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = connectTimeoutMs
            readTimeout = readTimeoutMs
            instanceFollowRedirects = true
            setRequestProperty("Accept", "application/json,text/plain,*/*")
            setRequestProperty("User-Agent", "DSU-Sideloader-Plus")
        }
}
