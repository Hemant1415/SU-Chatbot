<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>SUChatBot</title>  
    <link rel="stylesheet" href="/static/home.css">  
</head>  
<body>  

  <div class="navbar">  
    <div class="nav-buttons">  
        <button><a href="/">Home</a></button>  
        <button><a href="/about">AboutUs</a></button>  
        <button><a href="/contact">ContactUs</a></button>  
    </div>  
    <div class="site-name"><b>SUChatBot</b></div>  
  </div>  

  <!-- Chat container with scroll -->  
  <div class="chat-container">  
      {% for message in chat_history %}  
          <div class="chat-bubble user-bubble">{{ message.query }}</div>  
          <div class="chat-bubble bot-bubble">{{ message.response }}</div>  
          <form method="post" id="queryForm" action="/submitf">  
              <input type="hidden" name="query" value="{{message.query}}">  
              <input type="hidden" name="response" value="{{message.response}}">  
              <button type="submit" id="feedback">Send feedback</button>  
          </form>  
      {% endfor %}  
      <hr>  

      <div>  
        {% if remaining %

