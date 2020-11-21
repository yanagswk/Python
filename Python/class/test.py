class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        """ 平均成績
        """
        return sum(self.marks) / len(self.marks)

    @classmethod
    def friend(cls, origin, friend_name, *args):
        """
        同じ学校の友達を追加する。
        継承クラスで動作が変わるべき(継承クラスでは salaryプロパティがある)
        なのでclassmethodを使う。
        子クラスの初期化引数は *argsで受けるのがいい
        """
        return cls(friend_name, origin.school, *args)
    
    @staticmethod
    def say_hello():
        """
        先生に挨拶する
        継承しても同じ動きでいいのでstaticmethodを使う
        """
        print("Hello Teacher")
        

class WorkingStudent(Student):
    def __init__(self, name, school, salary):
        super().__init__(name, school)
        self.salary = salary


hiro = WorkingStudent("Hiro", "Stanford", 20.00)
mitsu = WorkingStudent.friend(hiro, "Mitsu", 15.00)
print(mitsu.salary)
