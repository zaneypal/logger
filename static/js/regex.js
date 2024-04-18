function regexSearch() {
    const query = document.getElementById('regex-query-search-bar').value;
    const file = document.getElementById('file-name').innerHTML;
    fetch('/test/'+file, {
        method: 'POST',
        body: new URLSearchParams({ pattern: query }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('live-search').innerHTML = data.results;
    });
}