function check_pass(event)
{
    var str = document.getElementById('password').value;
    // short password
    if (str.length < 4) {
        document.getElementById('error').innerHTML = "Short password";
        return false;
    //long password
    } else if (str.length > 20) {
        document.getElementById('error').innerHTML = "Very long password";
        return false;
    }
    // Must contain at least 1 letter and 1 number
    if ((str.search(/\d/) != -1) && str.search(/[a-zA-Z]/) != -1)
    {
        document.getElementById('error').innerHTML = "";
        return true;
    }
    else
    {
        document.getElementById('error').innerHTML = "Password must contain at least 1 alphabetical character and number";
        return false;
    }
    return true;
}

function confirm_pass(event)
{
    var pass = document.getElementById('password').value;
    var conf = document.getElementById('confirmation').value;
    console.log(pass);
    console.log(conf);
    // Check if passwords match
    if (conf == pass)
    {
        return true;
    }
    document.getElementById('error').innerHTML = "Passwords must match";
    return false;
}
// Enables register button only when passwords match and password passed check_pass function
function result(event)
{
    if (confirm_pass() && check_pass())
    {
        document.getElementById('sub').disabled = false;
        return;
    }
    return;
}


// Get backgrounds
async function get_bg(event)
{
    var choice = event.srcElement.value;
    console.log(choice);
    var bg = document.getElementById('bg')

    let response = await fetch("/rulebook");
    if (response.ok)
    {
        let res = await response.text();

        // Initialize the DOM parser
        var parser = new DOMParser();

        // Parse the text
        var doc = parser.parseFromString(res, "text/html");
        let art = doc.getElementById('chapter-4-wands-backgrounds-backgrounds-' + choice).innerHTML;
        bg.innerHTML = art;
        bg.removeChild(bg.lastElementChild)
    }

    return;
}

// Get house
async function get_house(event)
{
    var choice = event.srcElement.value;
    console.log(choice);
    var house = document.getElementById('house')

    let response = await fetch("/rulebook");
    if (response.ok)
    {
        let res = await response.text();

        // Initialize the DOM parser
        var parser = new DOMParser();

        // Parse the text
        var doc = parser.parseFromString(res, "text/html");
        let art = doc.getElementById('chapter-1-houses-races-' + choice).innerHTML;
        house.innerHTML = art;
        house.removeChild(house.lastElementChild)
    }

    return;
}

// Get style
async function get_style(event)
{
    var choice = event.srcElement.value;
    console.log(choice);
    var style = document.getElementById('style')

    let response = await fetch("/rulebook");
    if (response.ok)
    {
        let res = await response.text();

        // Initialize the DOM parser
        var parser = new DOMParser();

        // Parse the text
        var doc = parser.parseFromString(res, "text/html");
        // Insert data into div
        let art = doc.getElementById('the-' + choice + '-caster').innerHTML;
        style.innerHTML = art;
        style.removeChild(style.lastElementChild)
    }

    return;
}

// Get discipline
async function get_discipline(event)
{
    var choice = event.srcElement.value;
    console.log(choice);
    var discipline = document.getElementById('discipline')

    let response = await fetch("/rulebook");
    if (response.ok)
    {
        let res = await response.text();

        // Initialize the DOM parser
        var parser = new DOMParser();

        // Parse the text
        var doc = parser.parseFromString(res, "text/html");
        // Insert data into div
        let art = doc.getElementById('chapter-3-schools-of-magic-subclasses-' + choice).innerHTML;
        discipline.innerHTML = art;
        discipline.removeChild(discipline.lastElementChild)
    }

    return;
}

// Count points
function count_points(event)
{
    var arr = document.getElementsByClassName('abl');
    var remainder = 27;
    for (item of arr)
    {
        let point = item.value;
        let cost = calc_cost(point);
        console.log(point, cost);
        remainder -= cost;
    }
    document.getElementById('remaining').innerHTML = remainder;
    if (remainder < 0)
    {
        document.getElementById('error').innerHTML = 'You spent too many points';
    }
    else
    {
        document.getElementById('error').innerHTML = '';
    }
    if (remainder == 0)
    {
        document.getElementById('sub').disabled = false;
    }
    else
    {
        document.getElementById('sub').disabled = true;
    }
    return;
}

// Calculate points cost
function calc_cost(i)
{
    if (i <= 13)
    {
        return (i-8);
    }
    return ((i-13)*2 + 5);
}

// Abilities
var abilities = ['Strength', 'Dexterity', 'Intellect', 'Wisdom', 'Charisma', 'Constitution']
var adds = ['add_Str', 'add_Dex', 'add_Int', 'add_Wis', 'add_Cha', 'add_Con']
// Add additional ability points after house is chosen
function add_points(event)
{
    var house = event.srcElement.value;
    // Clear previous changes
    for (a of abilities)
    {
        document.getElementById(a).innerHTML = '';
    }
    for (ad of adds)
    {
        console.log(ad);
        document.getElementById(ad).value = 0;
    }
    // Set values
    if (house == 'gryffindor'){
        document.getElementById('Constitution').innerHTML += '+1';
        document.getElementById('add_Con').value = 1;
        document.getElementById('Charisma').innerHTML += '+1';
        document.getElementById('add_Cha').value = 1;
        // Change page theme
        document.getElementById('mid').style.backgroundColor = "#ffc500";
        let color = document.getElementById('mid').style.backgroundColor;
        console.log(color);
        document.getElementById('left').style.backgroundColor = "#7f0909";
        document.getElementById('right').style.backgroundColor = "#7f0909";
    }
    if (house == 'hufflepuff'){
        document.getElementById('Constitution').innerHTML += '+1';
        document.getElementById('add_Con').value = 1;
        document.getElementById('Wisdom').innerHTML = '+1';
        document.getElementById('add_Wis').value = 1;
        // Change page theme
        document.getElementById('mid').style.backgroundColor = "#eeba35";
        let color = document.getElementById('mid').style.backgroundColor;
        console.log(color);
        document.getElementById('left').style.backgroundColor = "#000000";
        document.getElementById('right').style.backgroundColor = "#000000";
    }
    if (house == 'slytherin'){
        document.getElementById('Charisma').innerHTML = '+1';
        document.getElementById('add_Cha').value = 1;
        document.getElementById('Dexterity').innerHTML = '+1';
        document.getElementById('add_Dex').value = 1;
        // Change page theme
        document.getElementById('mid').style.backgroundColor = "#aaaaaa";
        let color = document.getElementById('mid').style.backgroundColor;
        console.log(color);
        document.getElementById('left').style.backgroundColor = "#026217";
        document.getElementById('right').style.backgroundColor = "#026217";
    }
    if (house == 'ravenclaw'){
        document.getElementById('Intellect').innerHTML += '+1';
        document.getElementById('add_Int').value = 1;
        document.getElementById('Wisdom').innerHTML += '+1';
        document.getElementById('add_Wis').value = 1;
        // Change page theme
        document.getElementById('mid').style.backgroundColor = "#5d5d5d80";
        let color = document.getElementById('mid').style.backgroundColor;
        console.log(color);
        document.getElementById('left').style.backgroundColor = "#223164";
        document.getElementById('right').style.backgroundColor = "#223164";
    }
}




