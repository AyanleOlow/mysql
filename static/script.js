/* Her kan du putte JavaScript :) */
function sendData(id, type, data) {
    info = {
        id: id,
        type: type,
        data: data
    }
    fetch('/api/data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(info)
    })
    .then(response => response.json())
    .then(data => {
    document.getElementById('response').textContent = data.response;
    })
    .catch(err => console.error(err));
}