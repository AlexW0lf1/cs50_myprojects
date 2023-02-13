document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Use event instead default form submission
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show emails
  fetch(`/emails/${mailbox}`)
  .then(response => {
    console.log(response);
    return response.json();
  })
  .then(emails => {
    emails.forEach(get_email)
    return;
  })
}

// Event listener for sending email
function send_email() {
  recipients = document.querySelector('#compose-recipients').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(message => {
    console.log(message)
    if (message.error) {
      element = document.querySelector('#message');
      element.innerHTML = message.error;
      element.style.display = 'block';
    }
    else {
      element = document.querySelector('#message');
      element.innerHTML = message.message;
      element.style.display = 'block';
      load_mailbox('sent');
    }
  })
  return false;
};

// Get email
function get_email(email) {
  const element = document.createElement('div');
  element.innerHTML = `<div><b>${email.sender}</b>${email.subject}<span>${email.timestamp}</span></div>`;
  const id = parseInt(email.id);
  // Event listener to view email
  element.addEventListener('click', () => view_email(id));
  document.querySelector('#emails-view').append(element);
}

// View email
function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML = '';
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(data => {
    const element = document.createElement('div');
    element.innerHTML = `<div><p><b>From:</b> ${data.sender}</p><p><b>To:</b> ${data.recipients}</p><p><b>Subject:</b> ${data.subject}</p><p><b>Timestamp:</b> ${data.timestamp}</p></div>`;
    document.querySelector('#email-view').append(element);
    })
};