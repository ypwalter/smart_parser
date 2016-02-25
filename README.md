# Smart Parser

Smart Parser is a tool aimed to solve the issues of examining log. We want to build a software that can parse through any kind of information and come out with certain information we need.

## Installation

You need the following tool installed.
> [Tornado httpd official website](http://www.tornadoweb.org/en/stable/)
> [Python 2.7+](https://www.python.org/download/releases/2.7/)

## Working Phrase and Target

We have the following phrase as of 2016/02

### 1st Phrase
Proof of Concept: Making a basic library including "basic parser", "basic analyzer", and "output generator"
It can return the information parsed.

Basic Parser: simply parsing through the log
Basic Analyzer: simply analyzing the error and warning message with rule based system

Done 2016/02/16

### 2nd Phrase
Proof of Concept: "Basic feedback system" and "basic logging of feedback"
It can show you the information parsed in webpage and do some basic operating.

Basic Feedback System: the html format is still basic, but this include websocket for updating information
Basic Servers: httpd server and websocket server
Basic Logging of Feedback: sqlite library for storing data

Not yet finished. Planning to fix minor communication issues and webpage styling before 2016/03/04
Google Slide: http://tinyurl.com/SmartParser

### 3rd Phrase
Enhancement: "Basic feedback analyzing", "minimizing log", and "webpage improving"

Planning to finish it by end of March, 2016


