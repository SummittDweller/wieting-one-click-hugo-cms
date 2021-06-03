---
title: Contact Us
draft: false
author: Mackenzie McFate
date: 2021-03-31T07:50:29-05:00
socialshare: false
weight: 150
menu:
  main:
    identifier: contact
    parent: about
    weight: 850
---

## Interested in becoming a Wieting Theatre volunteer, OR booking an event, OR something else?

The Wieting has lots of opportunities for volunteers as EVERYONE at the theatre will atest. We also have ample opportunites to host your event, be it a dance, concert, play, wedding, lecture, meeting... you name it.

Please use this form to let us know how we can help you.  Be sure you include an email address or phone number, and someone, a Wieting volunteer, will contact you as soon as we are able.  Thank you!

<!-- If your interest is in becoming a Wieting Volunteer please use this online form to capture some sense of your interests and availability so we can make your service at the Wieting stress-free and fun.  We do our best to share information with you via this web site and through e-mail, so please provide us with an e-mail address if you have one.  If not, that's OK too.  We have several volunteers without e-mail so we also send out updates in the postal mail. -->

<form name="contact" method="POST" data-netlify="true">

  <fieldset>
   <legend>Your Contact Information</legend>
   <label>Name: <input type="text" name="name" /></label><br/>   
   <label>Email: <input type="email" name="email" /></label><br/>
   <label>Phone Number: <input type="phone" name="phone" /></label><br/>
  </fieldset>

  <fieldset>
    <legend>Your Interests</legend>
    <select name="interests[]" multiple>
      <option value="volunteer">Becoming a Wieting Volunteer</option>
      <option value="event">Book an Event at the Wieting</option>
      <option value="question">Any Other Question or Request</option>
    </select><br/>
    Select one or more of the interests listed above.<br/>
  </fieldset>

  <fieldset>
    <legend>Details</legend>
    <textarea name="details" rows="12" cols="60"></textarea></br>
    Use the space provided above to let us know how we can help.  Please provide as much detail as possible.
  </fieldset>

  <p><br/>
    <button type="submit">Send</button>
  </p>
</form>
