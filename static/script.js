let text_box = document.querySelector('.textBox');
let text_box2 = document.querySelector('.textBox2');
let message_box = document.querySelector('.message-box');
let rusExampleButton = document.querySelector('.btn-rus');
let engExampleButton = document.querySelector('.btn-eng');
let server_url = new URL('request', window.location.href).href;
const rusExamplePrompt = 'Сколько посылок прибыло в Москву?';
const rusExampleContext = 'CREATE TABLE Shipments (destination VARCHAR(50), weight INT)';
const engExamplePrompt = 'How much money was spent on toys?';
const engExampleContext = 'CREATE TABLE Expenses (category VARCHAR(30), cost INT, purchase_date DATE';

function submit() {
    let message = text_box.value;
    let context = text_box2.value;
    text_box.value = '';
    text_box2.value = '';

    fetch(server_url, {
        method: "POST",
        body: JSON.stringify({ prompt: message, context: context }),
        headers: {
            "Content-type": "application/json",
            "accept": "application/json",
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((json) => {
            message_box.innerHTML = json.answer + '\n\n';
        })
        .catch((error) => {
            console.error("Fetch error:", error);
            message_box.innerHTML += server + "Error: " + error.message + '\n\n';
        });
}

const rusExample = () => {
    text_box.value = rusExamplePrompt
    text_box2.value = rusExampleContext
}

const engExample = () => {
    text_box.value = engExamplePrompt
    text_box2.value = engExampleContext
}

rusExampleButton.addEventListener('click', () => {
    rusExample();
});

engExampleButton.addEventListener('click', () => {
    engExample();
});
