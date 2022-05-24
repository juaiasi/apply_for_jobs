function generateRandomPassword(range = 16){
    let password = ""
    let pw_range = range
    let random = Math.random
                        // remains: minimal number of characters needed for other types of characters
    let randomNumber = (remains) => Math.floor(random() * (pw_range - remains)) + 1
    
    // Sorting number of each type of character
    const numberOfLowers = randomNumber(3)
    const numberOfUppers = randomNumber(numberOfLowers + 2)
    const numberOfNumbers = randomNumber(numberOfLowers + numberOfUppers + 1)
    const numberOfSpecials = pw_range - numberOfLowers - numberOfUppers - numberOfNumbers
    
    let arrayStrings = [
        {
            string:'abcdefghijklmnopqrstuvxzwç',
            range:numberOfLowers
        },
        {
            string:'ABCDEFGHIJKLMNOPQRSTUVXZWÇ',
            range:numberOfUppers
        },
        {
            string:'1234567890',
            range:numberOfNumbers
        },
        {
            string:'!@#$%¨&*()_+-{}[]:;.>,<\\|/?\"\'¹²³£¢¬§ªº',
            range:numberOfSpecials
        },
    ]
    
    // Loops throught arrayStrings
    for (let i = 0; i < arrayStrings.length; i++){

        // Loops throught previously defined random intervals, that contains an specific type of string of characters
        for (let r = 0; r < arrayStrings[i].range; r++){

            let randomPosition = Math.floor(random() * arrayStrings[i].string.length)   // random Position of char inside specifc string
            let char = arrayStrings[i].string.charAt(randomPosition)                    // get char at random position
            password += char // Concatenate random char at password

            // Eliminating char, so there are no duplicates:
            arrayStrings[i].string = arrayStrings[i].string.replace(char,"")

        }
    }
    
    // Shuffle concatenated value
    password = password.split('').sort().join('');

    return arrayStrings
}    



console.log(generateRandomPassword())