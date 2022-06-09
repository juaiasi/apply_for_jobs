function generateRandomPassword(len = 16){
    // Function for generating randomic passwords with at least one character of each type, having the length provided as argument
    let password = "",
        pw_length = len,
        random = Math.random,
                        // remains: minimal number of characters needed for other types of characters
        randomNumber = (remains) => Math.floor(random() * (pw_length - remains)) + 1
    
    // Randomizing number of each type of character
    const numberOfLowers = randomNumber(3),
        numberOfUppers = randomNumber(numberOfLowers + 2),
        numberOfNumbers = randomNumber(numberOfLowers + numberOfUppers + 1),
        numberOfSpecials = pw_length - numberOfLowers - numberOfUppers - numberOfNumbers
    
    // Types of character strings
    let arrayStrings = [
        {
            string:'abcdefghijklmnopqrstuvxzwç',
            len:numberOfLowers
        },
        {
            string:'ABCDEFGHIJKLMNOPQRSTUVXZWÇ',
            len:numberOfUppers
        },
        {
            string:'1234567890',
            len:numberOfNumbers
        },
        {
            string:'!@#$%¨&*()_+-{}[]:;.>,<\\|/?\"\'¹²³£¢¬§ªº',
            len:numberOfSpecials
        },
    ]
    
    // Loops throught arrayStrings
    for (let i = 0; i < arrayStrings.length; i++){

        // Loops throught previously defined random intervals, that contains an specific type of string of characters
        for (let r = 0; r < arrayStrings[i].len; r++){

            let randomPosition = Math.floor(random() * arrayStrings[i].string.length),   // random Position of char inside specifc string
                char = arrayStrings[i].string.charAt(randomPosition)                    // get char at random position
            
            password += char // Concatenate random char at password

            // Eliminating char, so there are no duplicates:
            arrayStrings[i].string = arrayStrings[i].string.replace(char,"")

        }
    }
    
    // Shuffle concatenated value
    password = password.shuffle()

    document.querySelector("input#password").value = password
}

String.prototype.shuffle = function () {
    // Function for shuffle strings
    let arrayFromString = this.split(""),
        len = arrayFromString.length;

    for(let i = len - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        let tmp = arrayFromString[i]; //temporary var
        // Each one switches places with another in a random position:
        arrayFromString[i] = arrayFromString[j];
        arrayFromString[j] = tmp;
    }
    return arrayFromString.join("");
}

function copyText(query_text,query_btn,msg){
    /* Function to copy the text of a tag (query_text),
    activated by clicking the button (query_btn),
    that returns a message of success (msg) */

    // Check if query refers to the field that shows password, wich is an input. In that case, uses the "value" method. Else, uses "innerHTML"
    var content = query_text === "#pw"? document.querySelector(query_text).value : document.querySelector(query_text).innerHTML;
    // Copy
    navigator.clipboard.writeText(content)
    
    // Returns feedback with the chosen message
    var tooltip = document.querySelector(query_btn);
    tooltip.innerHTML = msg;
}
