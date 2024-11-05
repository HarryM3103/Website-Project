let page_loaded = false; //Global variable determining if the page has already been loaded with content

// TODO Finish documenting site.js

//Function that sends the user's search field data to the backend to be processed
function send_data() {
  document.querySelector(".searchContainer").style.position = "absolute"; //Sets the search box's position to 'absolute'
  document.querySelector(".searchContainer").style.top = "10%"; //Moves the search box to the top of the page
  document.querySelector(".searchContainer").style.transition = "0.5s"; //Adds a transition animation to the search box being moved to the top of the page
  if (page_loaded == true) {
    document.querySelector(".loader").style.visibility = "visible";
  } else {
    setTimeout(function () {
      document.querySelector(".loader").style.visibility = "visible";
    }, 500);
  }

  let item_type = document.getElementById("item_type").value;
  $.ajax({
    url: "/data_received",
    type: "POST",
    data: { name: item_type },
    // After the ajax 'POST' call is finished, call the ajax 'GET' function, receive_data()
  }).done(function () {
    receive_data();
    document.getElementById("item_type").value = "";
    document.querySelector(".items-table").innerHTML = "";
    document.querySelector(".table").style.visibility = "hidden";
  });
}

function receive_data() {
  $.ajax({
    url: "/data_sent",
    method: "GET",
    success: function (result) {
      parse_data(result);
    },
  });
}

function parse_data(data) {
  const items = document.querySelector(".items-table");
  for (let i = 0; i < data.length; i += 1) {
    if (items.innerHTML != "") {
      document.querySelector(".loader").style.visibility = "hidden";
    }
    // document.documentElement.style.setProperty('--rating', rating)
    let code = `\
        <tr onclick="window.open('${data[i][2]}', '_blank');">
            <td>${i+1}</td>
            <td><img src=${data[i][0]} alt=""></td>
            <td>${data[i][1]}</td>
            <td class="item-name">${data[i][3]}</td>
            <td>$${data[i][4]}</td>
            <td>${data[i][6]}%</td>
            <td>${data[i][8]}</td>
            <td>${data[i][9]}</td>
        </tr>
        `;
    items.innerHTML += code;
  }
  document.querySelector(".table").style.visibility = "visible";
  page_loaded = true;
}


