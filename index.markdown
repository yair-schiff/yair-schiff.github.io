---
layout: home
title: About Me
icon: fa-user
---
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
    .curve {
      width: 175px;
      height: 185px;
      float: left;
      shape-outside: circle();
      border-radius: 50%;
      margin: 15px;
      border-style: solid;
    }
    .wraptext p {
      text-align: left;
      padding-left: 215px;
      margin: 40px 0 0 7px;
      word-wrap: break-word;
    }
    @media only screen and (max-width: 768px) {
      .curve {
        width: 120px;
        height: 130px;
        float: None;
      }
    .wraptext p {
      padding-left: 10px;
    }
  }
  </style>
  </head>
  <body>
    <div class="wraptext">
    <img src="assets/images/profile_picture.jpeg" alt="profile_pictures" class="curve">
    <p>I am a PhD candidate in the Computer Science department at <a href="https://www.cs.cornell.edu/" target="_blank">Cornell University</a> where I am fortunate to be working with Prof. <a href="https://www.cs.cornell.edu/~kuleshov/" target="_blank"> Volodymyr Kuleshov</a>.
    <p>Here is my full <a style="font-weight:400" href="assets/resume/YSResume2026.pdf" target="_blank">CV</a>.</p>
    </div>
  </body>
</html>
