let date_1 = new Date();
let date_2 = new Date('09/15/2019');

let difference = date_1.getTime() - date_2.getTime();
console.log(difference);

let year = date_1.getFullYear()
document.getElementById("year").innerHTML = year

let TotalDays = Math.ceil(difference / (1000 * 3600 * 24));
let WorkingHours = TotalDays * 24 * 0.2 // to hours and then to 5hours a day avg
let TotalCoffee = WorkingHours / 3.4 // a coffee per 3 hours
let projects = WorkingHours * 0.002 // idk what calc this is. avg hours for a project
let happyClients = projects * 1.2 // avg happy clients per project

document.getElementById("WorkingHours").innerHTML = WorkingHours
document.getElementById("cofee_cups").innerHTML = TotalCoffee
document.getElementById("projects").innerHTML = projects
document.getElementById("happyClients").innerHTML = happyClients
