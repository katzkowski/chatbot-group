/**
 * Client-side script to receive, send and display messages.
 * Authors: ?, Katja Schneider, Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 20.05.2020
 */

import { closeSuggestions, userInput } from './suggestions.mjs';
import { closeSettings } from './settings.mjs';

let socket = io.connect("https://elephanture.informatik.uni-bremen.de:5000"),
  sendButton = document.getElementById('send-button'),
  userName = undefined,
  levelID = 'test_level_ID',
  senderName = 'test_sender_name',
  roomName = 'test_room_name',
  itemList = [{ item: 'test_item_name1', action: 'test_item_action1' }, { item: 'test_item_name2', action: 'test_item_action2' }],
  msg;

socket.on('connect', function () {
  console.log('connected client');
});


/**
 * Display received message from socket in chat interface.
 */
socket.on('json', (json) => {
  console.log('message received');
  msg = readJSON(json);

  updateRoomName(roomName);
  // updateCurrentLevel(levelID);
  printMessage(msg);
});


/**
 * Handle send button click event.
 */
sendButton.addEventListener('click', () => {
  userName == undefined ? sendUserName() : sendMessage();
}, false);


/**
 * Sends the message from the chat input to the socket.
 */
function sendMessage(evt = 'json') {
  let json;
  msg = userInput.value;

  // set user as sender on outgoing messages
  senderName = 'user';

  // store user name in client variables
  if (evt == 'user_registration') {
    userName = msg;
  }

  // send JSON String to socket
  if (msg.trim() != '') {
    json = createJSON(msg);
    socket.emit(evt, json);
    console.log('message ' + msg + ' has been sent!');
    userInput.value = null;
    closeSuggestions();

    printMessage(msg);
    userInput.focus();

  } else {
    console.log('no message to send!');
  }
}


/**
 * Prints the message into the chat.
 * @param {String} msg the message to print 
 */
function printMessage(msg) {
  let chat = document.getElementById('chat-content-container'),
    elem = window.document.createElement('li');

  elem.innerHTML = msg;

  // set message type depending on sender 
  switch (senderName) {
    case 'bot':
      elem.className = 'chat-message-bot';
      break;

    default:
      elem.className = 'chat-message-user';
      break;
  }

  chat.appendChild(elem);

  // scroll to bottom
  chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}


/**
 * Updates the room name.
 * @param {String} room  new room name 
 */
function updateRoomName(room) {
  let rName = document.getElementById('room_name');
  rName.innerHTML = room;
}


/**
 * Updates the currently level.
 * @param {String} level new level
 */
function updateCurrentLevel(level) {
  let currentLevel = document.getElementById('level');
  console.log(currentLevel);

  currentLevel.innerHTML = level;
}


/**
 * Creates a new JSON String using the data from client variables and the specified message.
 * @param {String} msg the message to be transported in the JSON String
 * @returns {JSON String} the generated JSON String 
 */
function createJSON(msg) {
  let obj, json;

  // create object to parse into JSON
  obj = {
    level: levelID,
    sender: senderName,
    room: roomName,
    items: itemList,
    message: msg
  };

  // parse object into JSON String
  json = JSON.stringify(obj);
  console.log('parsed JSON String: ' + json);

  return json;
}


/**
 * Reads a JSON String, stores its data in client variables and returns the message.
 * @param {JSON String} json the JSON String
 * @returns {String} the message transported in the JSON String 
 */
function readJSON(json) {
  // parse JSON String into JS object
  let message, obj = JSON.parse(json);
  console.log('received JSON String: ' + JSON.stringify(obj));

  // update client variables
  levelID = obj.level;
  senderName = obj.sender;
  roomName = obj.room;
  itemList = obj.items;
  message = obj.message;

  console.log('received message: ' + message);

  return message;
}


/**
 * Sends the user name to the server and changes the placeholder text.
 */
function sendUserName() {
  sendMessage('user_registration');
  userInput.placeholder = 'What will you do?';
}


/**
 * Close input field suggestions on click outside of input field.
 */
window.addEventListener('click', (evt) => {
  console.log(evt.target);

  console.log('window click');
  if (evt.target.id != 'input-user') closeSuggestions();
  if (!document.getElementById('settings-window').contains(evt.target) && evt.target.id != 'settings') closeSettings();
}, false);


window.addEventListener('keyup', (evt) => {
  evt.preventDefault(); //???????
});


export { sendButton }