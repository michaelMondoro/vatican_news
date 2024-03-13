var date = new Date()
if (date.getHours() > 15) {
    document.getElementsByTagName("html")[0].dataset.theme = "dark"
}
function summarize(e) {
    console.log(e.dataset.id)
    e.ariaBusy = "true"
    var link = document.getElementById(e.dataset.id)

    $.ajax({
    url: '/summarize?url=' + link.href,
    data: "",
    type: 'POST',
    success: function(response){
        p = document.createElement("footer");
        p.textContent = response['summary']
        e.parentElement.append(p)
        e.remove()
    },
    error: function(error){
        console.log(error);
        e.ariaBusy = "false"
    }
});
}   

function date_select(e) {
    dropdown = document.querySelector(".date_dropdown");
    dropdown.open = "";
    dropdown.childNodes[1].textContent = e.textContent;

    // Set articles display mode
    articles = document.getElementsByTagName('article');
    if (e.textContent == "All") {
        for (let i=0; i<articles.length; i++) {
            if (i >= 10) {
                a.classList.add('disabled')
            } else {
                a.classList.remove('disabled')
            }
        }
        return 
    }
    for (let i=0; i<articles.length; i++) {
        a = articles[i];
        if (!a.dataset.date.includes(e.textContent)) {
            a.classList.add('disabled')
        } else {
            a.classList.remove('disabled')
        }
    }
}




function load_more() {
    articles = document.getElementsByTagName('article');
    more = 0;
    for (let i=0; i<articles.length; i++) {
        a = articles[i];
        if (a.classList.contains("disabled")) {
            a.classList.remove("disabled");
            more += 1;
        }
        if (more == 10) {
            break;
        }
    }
}


// Load more when scroll hits bottom of page
// $(window).scroll(function () {
//     if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
//        load_more();
//     }
//  });