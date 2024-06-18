document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('file-input');

    formData.append('file', fileInput.files[0]);

    fetch('http://localhost:5001/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        fileInput.value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('recognize-btn').addEventListener('click', function() {
    fetch('http://localhost:5001/recognize', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerText = data.error;
            } else {
                document.getElementById('result').innerText = `Welcome ${data.name}!`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
