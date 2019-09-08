# librarian

This is an application with the following functions:

- Manage the books on your bookshelf
  - Register your books in the database
- Manage members who can borrow your books
  - Register people who can borrow books on your bookshelf in the database
- Manage book lending and borrowing
  - For lenders
    - Tell you book's state (available or lending)
    - Tell you who borrows which book
    - Memorize book lending history
  - For borrowers
    - Tell you books which you are borrowing
    - Tell you when you should return the book
    - Memorize book lending history

## Register Books

- Capture your book's ISBN
- Get book's title from Google Books API
- Register book's information in the database

## Register Members

- Load member information csv format (id, name_jp, name_en)
- Register member information in the database
- Save member ID information as QR code

## Borrowing Procedure

- Capture your ID QR code, then app starts the procedure
- Capture books' barcode you want to borrow
- Enter terminate command
- App enters standby

## Browsing book lending history (admin)

- comming soon ...

## Browing book borrowing history (member)

- comming soon ...
