// Listen to events (form submit)

document.addEventListener('submit', async function(event){
    var ev = event.srcElement;
    console.log(ev.innerHTML);
    var hits = [{style: 'willpower', hit_dice: 'd10', hp_1: 10, hp_after: 6},
    {style: 'technique', hit_dice: 'd6', hp_1: 6, hp_after: 4},
    {style: 'intellect', hit_dice: 'd8', hp_1: 8, hp_after: 5}]
    var willpower = {'hit dice': 'd10', 'hp_1': 10, 'hp_after': 6};
    var technique = {'hit dice': 'd6', 'hp_1': 6, 'hp_after': 4};
    var intellect = {'hit dice': 'd8', 'hp_1': 8, 'hp_after': 5};
    // Prevent page from refreshing if event not from 'stop session' form
    if (ev.id != 'stop')
    {
        event.preventDefault();
        // grab the data inside the form fields
        const formData = new FormData(ev);
        console.log(formData);
        const name = formData.get("session_name")
        // Prevent server request for lvlup if level = 20
        const level = formData.get("level");
        const player_id = formData.get("player_id");
        if (level)
        {
            let p_lvl = parseInt(document.getElementById('p_lvl_' + player_id).innerHTML);
            if (p_lvl == 20)
            {
                alert('Max level!');
                return;
            }
        }
        // Request successfully sent!
        var response = await fetch('/sessions/session/' + name, {
            method: 'POST',
            body: formData,
        });
        console.log(response);
        if (response.ok)
        {
            //change value on page
            const dmg_hl = formData.get("dmg_hl");
            const num = parseInt(formData.get("num"));
            // If damage/heal form triggered
            if (dmg_hl)
            {
                var max_hp = parseInt(document.getElementById('max_hp_' + player_id).innerHTML);
                var hp = parseInt(document.getElementById('cur_hp_' + player_id).innerHTML);
                if (dmg_hl == 'd')
                {
                    hp = hp - num;
                    document.getElementById('cur_hp_' + player_id).innerHTML = hp;
                    var dif = max_hp - hp;
                    document.getElementById('heal_' + player_id).max = dif.toString();
                    document.getElementById('damage_' + player_id).value = "0";
                    console.log(document.getElementById('heal').max)
                    return;
                }
                else
                {
                    hp = hp + num;
                    document.getElementById('cur_hp_' + player_id).innerHTML = hp;
                    var dif = max_hp - hp;
                    document.getElementById('heal_' + player_id).max = dif.toString();
                    document.getElementById('heal_' + player_id).value = "0";
                    console.log(document.getElementById('heal').max);
                    return;
                }
            }
            // If level form triggered
            if (level == 'level')
            {
                var p_lvl = parseInt(document.getElementById('p_lvl_' + player_id).innerHTML);
                p_lvl = p_lvl + 1;
                // If level 20 disable levelup button
                if (p_lvl == 20)
                {
                    document.getElementById('p_' + player_id).disabled = true;
                }
                document.getElementById('p_lvl_' + player_id).innerHTML = p_lvl;
                // Set hp value
                const con = parseInt(formData.get("con"));
                const style = formData.get("cast_style");
                for (el of hits)
                {
                    if (el.style == style)
                    {
                        var max_hp = el.hp_1 + (p_lvl - 1)*(el.hp_after + con);
                        document.getElementById('max_hp_' + player_id).innerHTML = max_hp;
                        document.getElementById('cur_hp_' + player_id).innerHTML = max_hp;
                        return;
                    }
                }
            }
        }
        else
        {
            alert("Error HTTP:" + response.status);
            return;
        }
    }
});

// Player side
// Get changes from server
window.addEventListener('load', async function check_param(event){
    const session_name = await document.getElementById('session_name').innerHTML;
    const role = await document.getElementById('role').innerHTML;
    const log = document.getElementById("log");
    const u_name = document.getElementById("u_name");
    // Send request to server
    let response = await fetch('/sessions/session/' + session_name);
    if (response.ok)
    {
        let res = await response.text();

        // Initialize the DOM parser
        var parser = new DOMParser();

        // Parse the text
        var doc = parser.parseFromString(res, "text/html");
        if (role == 'player')
        {
            // Look for changes for player
            // Current hp
            let old_hp = parseInt(document.getElementById('my_cur_hp').innerHTML);
            let new_hp = parseInt(doc.getElementById('my_cur_hp').innerHTML);
            if (old_hp != new_hp)
            {
                // Show changes in log
                let newNode = document.createElement("p");
                if (old_hp > new_hp)
                {
                    let dif = old_hp - new_hp;
                    let textNode = document.createTextNode('You '+ 'got ' + dif + ' damage');
                    document.getElementById('my_cur_hp').innerHTML = new_hp;
                    newNode.appendChild(textNode);
                    log.insertBefore(newNode, log.children[0]);
                    log.children[0].style.color = 'red';
                }
                else
                {
                    let dif = new_hp - old_hp;
                    let textNode = document.createTextNode('You' + ' healed for ' + dif);
                    document.getElementById('my_cur_hp').innerHTML = new_hp;
                    newNode.appendChild(textNode);
                    log.insertBefore(newNode, log.children[0]);
                    log.children[0].style.color = 'green';
                }
            }
            // Max_hp
            old_hp = document.getElementById('my_max_hp').innerHTML;
            new_hp = doc.getElementById('my_max_hp').innerHTML;
            if (old_hp != new_hp)
            {
                document.getElementById('my_max_hp').innerHTML = new_hp;
            }
            // Level
            let old_lvl = document.getElementById('my_lvl').innerHTML;
            let new_lvl = doc.getElementById('my_lvl').innerHTML;
            if (old_lvl != new_lvl)
            {
                document.getElementById('my_lvl').innerHTML = new_lvl;
                // Show changes in log
                let newNode = document.createElement("p");
                let textNode = document.createTextNode('You' + ' leveled up!');
                newNode.appendChild(textNode);
                log.insertBefore(newNode, log.children[0]);
                log.children[0].style.color = 'blue';
            }
            // Check stop message
            if (doc.getElementById('stop'))
            {
                // Show stop message in log
                let newNode = document.createElement("p");
                let textNode = document.createTextNode('Session is stopped!');
                newNode.appendChild(textNode);
                log.insertBefore(newNode, log.children[0]);
                log.children[0].style.color = 'gray';
            }
            // Look for changes for the rest of the party
            var id_arr = document.getElementsByClassName('p_ids');
            for (el of id_arr)
            {
                // Get player_id
                let id = el.children[0].innerHTML;
                // Get player name
                let p_name = el.children[1].innerHTML;
                // Do changes for this player by id
                // Current hp
                let old_hp = parseInt(document.getElementById('cur_hp_' + id).innerHTML);
                let new_hp = parseInt(doc.getElementById('cur_hp_' + id).innerHTML);
                if (old_hp != new_hp)
                {
                    // Show changes in log
                    let newNode = document.createElement("p");
                    if (old_hp > new_hp)
                    {
                        let dif = old_hp - new_hp;
                        let textNode = document.createTextNode(p_name + ' got ' + dif + ' damage');
                        document.getElementById('cur_hp_' + id).innerHTML = new_hp;
                        newNode.appendChild(textNode);
                        log.insertBefore(newNode, log.children[0]);
                        log.children[0].style.color = 'red';
                    }
                    else
                    {
                        let dif = new_hp - old_hp;
                        let textNode = document.createTextNode(p_name + ' healed for ' + dif);
                        document.getElementById('cur_hp_' + id).innerHTML = new_hp;
                        newNode.appendChild(textNode);
                        log.insertBefore(newNode, log.children[0]);
                        log.children[0].style.color = 'green';
                    }
                }
                // Max_hp
                old_hp = document.getElementById('max_hp_' + id).innerHTML;
                new_hp = doc.getElementById('max_hp_' + id).innerHTML;
                if (old_hp != new_hp)
                {
                    document.getElementById('max_hp_' + id).innerHTML = new_hp;
                }
                // Level
                let old_lvl = document.getElementById('lvl_' + id).innerHTML;
                let new_lvl = doc.getElementById('lvl_' + id).innerHTML;
                if (old_lvl != new_lvl)
                {
                    // Show changes in log
                    document.getElementById('lvl_' + id).innerHTML = new_lvl;
                    let newNode = document.createElement("p");
                    let textNode = document.createTextNode(p_name + ' leveled up!');
                    newNode.appendChild(textNode);
                    log.insertBefore(newNode, log.children[0]);
                    log.children[0].style.color = 'blue';
                }
            }
        }
        else
        {
            // No get requests for gm
            return;
        }
    }
    else
    {
        alert('Error HTTP: ' + response.status);
    }
    // Wait 3 seconds for next call
    // https://masteringjs.io/tutorials/fundamentals/wait-1-second-then
    await new Promise(resolve => setTimeout(resolve, 3000));
    check_param(event);
});

// Modal call
function open_modal(p_id)
{
    document.getElementById("modal_" + p_id).style.display = "block";

}

function close_modal(p_id)
{
    document.getElementById("modal_" + p_id).style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
var modals = document.getElementsByClassName("modal");
window.onclick = function(event) {
    for (modal of modals){
        if (event.target == modal){
            modal.style.display = "none";
        }
    }
  } 