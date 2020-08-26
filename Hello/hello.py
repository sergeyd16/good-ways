msg = "hello World"
print(msg)
msg2 = msg.capitalize()
print(msg2)
msg3 = msg2.split()
print(msg3)
email = "Anatoly Hairolin <anatolyh@checkpoint.com>; Ariel Suvorov <arielsu@checkpoint.com>; Assaf Darshan <assafda@checkpoint.com>; Bogdan Kirylyuk <bogdank@checkpoint.com>; Gilad Seror <giladsr@checkpoint.com>; Jan Ashkenazi <janash@checkpoint.com>; Jenny Glushkin <jennyg@checkpoint.com>; Yarden Yakobov <yardenya@checkpoint.com>"
emaillist = email.split(";")
print (emaillist)

mylist = []
for emailitem in emaillist:
    pureemail = emailitem[emailitem.find("<")+1:emailitem.find(">")]
    mylist.append(pureemail)
    print (pureemail)


