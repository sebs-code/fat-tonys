// Contact Form & Newsletter
AWS.config.region = 'eu-west-1';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'eu-west-1:f13e5e55-819c-404c-8f12-990c8b2ad7e4',
})

var LPAWS = {}
LPAWS.sendToNewsletter = function() {
    var sns = new AWS.SNS()
    var params = {
        Message: 'Email: ' + document.querySelector('#email').value,
        Subject: "Fat Tony's Newsletter",
        TopicArn: 'arn:aws:sns:eu-west-1:795528625754:Incerto_Contact_Form'
    }

    sns.publish(params, function(err, data) {
        if (err) console.log('error' + err, err.stack)  // an error occurred
        else     console.log('success' + data)            // successful response
    })
}

LPAWS.sendToContact = function() {
    var sns = new AWS.SNS()
    var params = {
        Message: 'Name: ' + document.querySelector('#contact-name').value + '\n' +'Email: ' + document.querySelector('#contact-email').value + '\n' +'Message: ' + document.querySelector('#message').value,
        Subject: "Fat Tony's Contact Form",
        TopicArn: 'arn:aws:sns:eu-west-1:795528625754:Incerto_Contact_Form'
    }

    sns.publish(params, function(err, data) {
        if (err) console.log('error' + err, err.stack)  // an error occurred
        else     console.log('success' + data)            // successful response
    })
}

function sendNewsletterForm(){
    var newsletterForm = document.getElementById("newsletterForm")

    // Validate
    if (newsletterForm.checkValidity() === false){
        newsletterForm.reportValidity()
        return
    }

    LPAWS.sendToNewsletter()

    // Show modal
    let newsletterModal = document.getElementById('newsletterModal')
    let modal = bootstrap.Modal.getOrCreateInstance(newsletterModal)
    modal.show()

    // Clear form
    newsletterForm.reset()
}


function sendContactForm(){
    var contactForm = document.getElementById("contactForm")

    // Validate
    if (contactForm.checkValidity() === false){
        contactForm.reportValidity()
        return
    }

    LPAWS.sendToContact()

    // Show modal
    let contactModal = document.getElementById('contactModal')
    let modal = bootstrap.Modal.getOrCreateInstance(contactModal)
    modal.show()

    // Clear form
    contactForm.reset()
}


function showBook(title, author, image, link, provider){
    // Afiiliate tag
    affiliate = "/ref=nosim?tag=fattonys07-20"

    // Set book title
    document.getElementById("bookTitle").innerHTML = title
    document.getElementById("bookAuthor").innerHTML = author
    document.getElementById("bookImage").src = '/theme/books/' + image
    document.getElementById("bookLink").href = link + affiliate
    document.getElementById("bookLink").innerHTML = 'View on ' + provider

    // Show modal
    let bookModal = document.getElementById("bookModal")
    let modal = bootstrap.Modal.getOrCreateInstance(bookModal)
    modal.show()
}

function updateQuoteHeader(name) {
    let quoteHeaderText = 'Quotes | ' + name
    let quoteHeader =document.getElementById("quote-header").innerHTML = quoteHeaderText
    if (name === 'All') {document.title =  "Quotes | Fat Tony's"} else {document.title =  name + " Quotes | Fat Tony's"}

}

function updateAuthorHeader(name) {
    let authorHeaderText = 'Antilibrary | ' + name
    let authorHeader =document.getElementById("antilibrary-header").innerHTML = authorHeaderText
    if (name === 'All') {document.title =  "Antilibrary | Fat Tony's"} else {document.title =  name + " | Antilibrary | Fat Tony's"}
}