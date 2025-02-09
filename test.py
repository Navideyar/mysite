password = input("Enter your password here: ")

if ( password.count ("") >= 9 ) and ( "@" or "!" in password)  :
    print ( "password ok" )
else :
    print ( "password too weak, return" )