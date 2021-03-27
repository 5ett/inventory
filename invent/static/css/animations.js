const back = document.querySelector(".grocery-back");
const login = document.querySelector(".login");
const tag1 = document.querySelector(".grocery-back-nosplit");
const tag2 = document.querySelector(".index-no-split");
const logo = document.querySelector(".logo");
const header1 = document.querySelector(".header1");
const header2 = document.querySelector(".header2");



const tl = new TimelineMax();

tl.fromTo(back,1, {height: "20vh"}, {height:"100vh", ease: Power2.easeInOut})
tl.fromTo(login, 0.7, {opacity:0, x:30}, {opacity:1, x:0}, "-=0.3")
tl.fromTo(tag1, 1, {height: "20%"}, {height:"100%"})
tl.fromTo(tag2, 1, {height: "20%"}, {height:"100%"}, "-=1")
tl.fromTo(logo, 0.7, {opacity:0, x:30}, {opacity:1, x:0}, "-=0.2")
tl.fromTo(header1, 1, {opacity:0, y:30}, {opacity:1, y:0})
tl.fromTo(header2, 0.8, {opacity:0, x:30}, {opacity:1, x:0}, "-=0.2");

