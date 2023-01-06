function getComm() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/comm");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" +  "<a href=\"/" + arr[i] + "\"" + ">" + arr[i] + "</a></td>"
     
      finalString = finalString + "</tr>"
      
    }
    
    document.getElementById("display.tbody").innerHTML = finalString;
  }
}


function getCommOfUser() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/user/comm");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" +  "<a href=\"/" + arr[i] + "\"" + ">" + arr[i] + "</a></td>"
      finalString = finalString + "<td>" + "<button type=\"button\">unjoin</button>" + "</td>" 
      finalString = finalString + "</tr>"
      
    }
    
    document.getElementById("display").innerHTML = finalString;
  }

}

function getPostOfUser() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/user/post");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.employees.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" +  "<a href=\"/" + arr.employees[i].community + "\"" + ">" + arr.employees[i].community + "</a></td>"
      finalString = finalString + "<td>" +  "<a href=\"/comm/" + arr.employees[i].id + "\"" + ">" + arr.employees[i].title + "</a></td>"
      finalString = finalString + "<td> " + arr.employees[i].title + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].body + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].date + "</td>"
      finalString = finalString + "<td>" + "<button onclick=\"deletePost(" + arr.employees[i].id +  ");\" id = \"deletepost\" type=\"button\">Delete</button>" + "</td>" 
      finalString = finalString + "</tr>"
      
    }
    
    document.getElementById("display").innerHTML = finalString;
  }
}

function getPostOfComm() {

  const xhttp = new XMLHttpRequest();
  let community = document.getElementById("community").innerHTML;
  url = "/" + community + "/post"
  xhttp.open("GET", url);
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.employees.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" +  "<a href=\"/Boxing/" + arr.employees[i].id + "\"" + ">" + arr.employees[i].title + "</a></td>"
      finalString = finalString + "<td>" + arr.employees[i].user + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].body + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].date + "</td>"
      finalString = finalString + "</tr>"
      
    }
    
    document.getElementById("display").innerHTML = finalString;
  }
}

function getPostForProfile() {

  const xhttp = new XMLHttpRequest();
  let community = document.getElementById("user").innerHTML;
  url = "/user/post/view/" + community
  xhttp.open("GET", url);
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.employees.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" +  "<a href=\"/Boxing/" + arr.employees[i].id + "\"" + ">" + arr.employees[i].title + "</a></td>"
      finalString = finalString + "<td>" + arr.employees[i].user + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].body + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].date + "</td>"
      finalString = finalString + "</tr>"
      
    }
    
    document.getElementById("display").innerHTML = finalString;
  }
}

function deletePost(postID) {

  let url = "/user/";
  let finalUrl = url + postID;

  const xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", finalUrl);
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.employees.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" + "<button onclick=\"deletePost(" + arr.employees[i].id +  ");\" id = \"deletepost\" type=\"button\">Delete</button>" + "</td>" 
      finalString = finalString + "<td> " + arr.employees[i].community + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].title + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].body + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].date + "</td>"
      finalString = finalString + "</tr>"
    }
    document.getElementById("display").innerHTML = finalString;
  }
  
}

function getPost() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/post");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    for(let i = 0; i < arr.employees.length; i++){
      console.log(arr[i]);
      finalString = finalString + "<tr>"
      finalString = finalString + "<td>" + "<button onclick=\"deletePost(" + arr.employees[i].id +  ");\" id = \"deletepost\" type=\"button\">Delete</button>" + "</td>" 
      finalString = finalString + "<td> " + arr.employees[i].community + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].title + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].body + "</td>"
      finalString = finalString + "<td> " + arr.employees[i].date + "</td>"
      finalString = finalString + "</tr>"
    }
    document.getElementById("display").innerHTML = finalString;
  }
}

function getSinglePost() {

  const xhttp = new XMLHttpRequest();
  let community = document.getElementById("postname").innerHTML;
  url = "/post/single/" + community
  xhttp.open("GET", url);
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    var arr = JSON.parse(str);
    var  finalString= "";
    finalString = finalString + "<tr>" 
    finalString = finalString + "<td>" +  "<a href=\"/" + arr.employees.community + "\"" + ">" + arr.employees.community + "</a></td>"
    finalString = finalString + "<td>" +  "<a href=\"/Boxing/" + arr.employees.id + "\"" + ">" + arr.employees.title + "</a></td>"
    finalString = finalString + "<td> " + arr.employees.body + "</td>"
    finalString = finalString + "<td> " + arr.employees.date + "</td>"
    finalString = finalString + "</tr>"
    
    document.getElementById("display").innerHTML = finalString;
  }
}

function getPostFromComm() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/comm/");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    document.getElementById("display").innerHTML = str;
  }
}

function getCurrentUser() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/user");
  xhttp.send();

  xhttp.onload = function() {
    let str = this.responseText;
    document.getElementById("display").innerHTML = str;
  }
}



function addGrade() {

  let url = "/Dogs/post";
  let post = document.getElementById("inputId").value;
 

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", url);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.onload = function() {
    let str = this.responseText;

    document.getElementById("display").innerHTML = str;
  }

  const body= {"post": post};
  xhttp.send(JSON.stringify(body));

}