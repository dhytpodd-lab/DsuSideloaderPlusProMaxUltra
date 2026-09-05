echo "Status of upload:"
grep -o "https://gofile.io/d/.*" /tmp/upload_output || echo "Waiting..."
