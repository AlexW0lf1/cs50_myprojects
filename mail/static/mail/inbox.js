document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
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

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json)
  .then(emails.forEach(email => {
    const element = () => {
      return `<div><b>${email.sender}</b>${email.subject}<span>${email.timestamp}</span></div>`;
    }
    const id = email.id;
    // Event listener to view email
    element.addEventListener('click', function(id) {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'block';
      fetch(`/emails/${id}`)
      .then(response => response.json)
      .then(data => {
        const e = () => {
          return `<div><p><b>From:</b> ${data.sender}</p><p><b>To:</b> ${data.recipients}</p><p><b>Subject:</b> ${data.subject}</p><p><b>Timestamp:</b> ${data.timestamp}</p></div>`;
        }
        document.querySelector('#email.view').append(e);
      })
    });
    document.querySelector('#emails-view').append(element);
  }))
}

// Event listener for sending email
document.querySelector('#compose-form').addEventListener('submit)', () => {
  fetch('/emails/', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').innerHTML,
      subject: document.querySelector('#compose-subject').innerHTML,
      body: document.querySelector('#compose-body').innerHTML
    })
  })
  .then(response => response.json)
  .catch(() => {
    element = document.querySelector('#message');
    element.innerHTML = message.message;
    element.style.display = 'block';
    return Promise.reject(Error(response.status))
  })
  .then(message => {
    load_mailbox('sent');
    element = document.querySelector('#message');
    element.innerHTML = message.message;
    element.style.display = 'block';
  })
});

//