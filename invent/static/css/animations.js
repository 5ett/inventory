const back = document.querySelector(".grocery-back");
const login = document.querySelector(".login");
const tag1 = document.querySelector(".grocery-back-nosplit");
const tag2 = document.querySelector(".index-no-split");
const logo = document.querySelector("#logo");



const tl = new TimelineMax();

tl.fromTo(back,1, {height: "20vh"}, {height:"100vh", ease: Power2.easeInOut})
.fromTo(login, 0.7, {opacity:0, x:30}, {opacity:1, x:0}, "-=0.3")
.fromTo(tag1, 1, {height: "20%"}, {height:"100%"})
.fromTo(tag2, 1, {height: "20%"}, {height:"100%"}, "-=1")
.fromTo(logo, 0.7, {opacity:0, x:30}, {opacity:1, x:0}, "-=0.2");

