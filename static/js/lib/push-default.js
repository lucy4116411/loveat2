/* global messaging */

messaging.onMessage((payload) => {
  // start show notification
  const notificationTitle = payload.data.title;
  const notificationOptions = {
    body: payload.data.content,
    icon: '/favicon.ico',
  };
  const notification = new Notification(notificationTitle, notificationOptions);
  // deal with click event
  notification.onclick = () => {
    window.open(payload.data.url);
  };
});
