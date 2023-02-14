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
  document.querySelector('#message').style.display = 'none';

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
  document.querySelector('#message').style.display = 'none';

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
      load_mailbox('sent');
      element.innerHTML = message.message;
      element.style.display = 'block';
    }
  })
  return false;
};

// Get email
function get_email(email) {
  const element = document.createElement('div');
  if (email.read) {
    element.innerHTML = `<div class="email-preview-gray"><b>${email.sender}</b>${email.subject}<span class="timestamp">${email.timestamp}</span></div>`;
  }
  else {
    element.innerHTML = `<div class="email-preview-white"><b>${email.sender}</b>${email.subject}<span class="timestamp">${email.timestamp}</span></div>`;
  }
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
  document.querySelector('#message').style.display = 'none';
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(data => {
    const element = document.createElement('div');
    element.innerHTML = `<div><p><b>From:</b> ${data.sender}</p><p><b>To:</b> ${data.recipients}</p><p><b>Subject:</b> ${data.subject}</p><p><b>Timestamp:</b> ${data.timestamp}</p><p class="pre"> ${data.body} </p><button id="reply" class="btn btn-sm btn-outline-primary">Reply</button></div>`;
    if (document.querySelector('#emails-view h3').innerHTML == 'Inbox') {
      element.innerHTML += `<button id="archive" class="btn btn-sm btn-outline-primary">Archive</button>`
      element.querySelector('#archive').onclick = () => archive(id);
    } else if (document.querySelector('#emails-view h3').innerHTML == 'Archive') {
      element.innerHTML += `<button id="archive" class="btn btn-sm btn-outline-primary">Unarchive</button>`
      element.querySelector('#archive').onclick = () => unarchive(id);
    }
    document.querySelector('#email-view').append(element);
    document.querySelector('#reply').onclick = () => reply(data);
    // Mark email as read
    fetch(`emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    })
};

function reply(data) {
  compose_email();
  // Fill composition fields
  document.querySelector('#compose-recipients').value = data.sender;
  document.querySelector('#compose-subject').value = data.subject.includes('RE:') ? data.subject : `RE:${data.subject}`;
  document.querySelector('#compose-body').value = `\nOn ${data.timestamp} ${data.sender} wrote:\n ${data.body}\n`;
}

function archive(id) {
  // Mark email as archived
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .then(response => {
    load_mailbox('inbox');
  })
}


function unarchive(id) {
  // Mark email as read
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .then(response => {
    load_mailbox('inbox');
  })
}