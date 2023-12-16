function produceNewspaper() {
    var topics = [];
    for (var i = 1; i <= 4; i++) {
        var topic = document.getElementById('topic' + i).value.trim();
        if (topic) {
            topics.push(topic);
        }
    }

    if (topics.length < 4) {
        alert('Please fill in all four topics.');
        return;
    }

    fetch('http://localhost:8000/generate_newspaper', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(topics)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Process and display the newspaper data here
        displayNewspaper(data);
    })
    .catch((error) => {
        console.error('Error:', error);

    });
}
window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('produceNewspaper').addEventListener('click', produceNewspaper);
});


function displayNewspaper(data) {
    // Assuming 'data.path' contains the URL/path to the generated newspaper
    if (data.path) {
        window.location.href = data.path;
    } else {
        console.error('Error: Newspaper path not found');
    }
}
