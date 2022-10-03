class Student:
    def __init__(self, data):
        [rnumber, fname, lname, email, dob, address] = [ x.strip() for x in data[:6]]
        self.__rnumber = rnumber
        self.__fname = fname
        self.__lname = lname
        self.__email = email
        self.__dob = dob
        self.__address = address
        self.__score = data[6]

    def data(self, update = False):
        data = (self.__fname, self.__lname, self.__email, self.__dob, self.__address, self.__score)
        return  data + (self.__rnumber,) if update else (self.__rnumber,) + data

    def dump(self):
        return {
            'roll_number' : self.__rnumber,
            'first_name' : self.__fname,
            'last_name' : self.__lname,
            'email' : self.__email,
            'date_of_birth' : self.__dob,
            'address' : self.__address,
            'score' : self.__score
        }

    @property
    def rnumber(self): return self.__rnumber

    @rnumber.setter
    def rnumber(self, x): self.__rnumber = x

    @property
    def fname(self): return self.__fname

    @fname.setter
    def fname(self, x): self.__fname = x

    @property
    def lname(self): return self.__lname

    @lname.setter
    def lname(self, x): self.__lname = x

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, x): self.__email = x

    @property
    def dob(self): return self.__dob

    @dob.setter
    def dob(self, x): self.__dob = x

    @property
    def address(self): return self.__address

    @address.setter
    def address(self, x): self.__address = x

    @property
    def score(self): return self.__score

    @score.setter
    def score(self, x): self.__score = x
