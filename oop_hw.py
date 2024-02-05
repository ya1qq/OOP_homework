class Student:
  def __init__(self, name, surname, gender):
    self.name = name
    self.surname = surname
    self.gender = gender
    self.finished_courses = []
    self.courses_in_progress = []
    self.grades = {}
  
  def _avg_grade(self):
    if not self.grades:
      return 0
    grades_list = []
    for i in self.grades.values():
      grades_list.extend(i)
    return round(sum(grades_list) / len(grades_list), 1)

  def __gt__(self, other):
    if isinstance(other, Student):
      if self._avg_grade() > other._avg_grade():
        return f'Средняя оценка {self.name} {self.surname} выше чем у {other.name} {other.surname}.'
      elif self._avg_grade() < other._avg_grade():
        return f'Средняя оценка {self.name} {self.surname} ниже чем у {other.name} {other.surname}.'
      else:
        return f'Средняя оценка {self.name} {self.surname} равна средней оценке {other.name} {other.surname}.'
    else:
      return 'Ошибка сравнения, объекты не являются студентами.'
        
  def __str__(self):
    return (
      f'Имя: {self.name}\n'
      f'Фамилия: {self.surname}\n'
      f'Средняя оценка за домашние задания: {self._avg_grade()}\n'
      f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
      f'Завершенные курсы: {", ".join(self.finished_courses)}'
    )
    
  def add_courses(self, course_name):
    self.finished_courses.append(course_name)

  def rate_lecturer(self, lecturer, course, grade):
    if (
      isinstance(lecturer, Lecturer) and course in self.courses_in_progress 
      and course in lecturer.courses_attached
    ):
      if course in lecturer.grades:
        lecturer.grades[course] += [grade]
      else:
        lecturer.grades[course] = [grade]
    else:
      return 'Ошибка.'

class Mentor:
  def __init__(self, name, surname):
    self.name = name
    self.surname = surname
    self.courses_attached = []

  def __str__(self):
    return f'Имя: {self.name}\nФамилия: {self.surname}'
  
class Lecturer(Mentor):
  def __init__(self, name, surname):
    super().__init__(name, surname)
    self.grades = {}

  def _avg_grade(self):
    if not self.grades:
      return 0
    grades_list = []
    for i in self.grades.values():
      grades_list.extend(i)
    return round(sum(grades_list) / len(grades_list), 1)

  def __gt__(self, other):
    if isinstance(other, Lecturer):
      if self._avg_grade() > other._avg_grade():
        return f'Средняя оценка {self.name} {self.surname} выше чем у {other.name} {other.surname}.'
      elif self._avg_grade() < other._avg_grade():
        return f'Средняя оценка {self.name} {self.surname} ниже чем у {other.name} {other.surname}.'
      else:
        return f'Средняя оценка {self.name} {self.surname} равна средней оценке {other.name} {other.surname}.'
    else:
      return 'Ошибка сравнения, объекты не являются лекторами.'

  def __str__(self):
    return super().__str__() + f'\nСредняя оценка за лекции: {self._avg_grade()}'
  
class Reviewer(Mentor):
  def __init__(self, name, surname):
    super().__init__(name, surname)

  def rate_hw(self, student, course, grade):
    if (
      isinstance(student, Student) and course in self.courses_attached 
      and course in student.courses_in_progress
    ):
      if course in student.grades:
        student.grades[course] += [grade]
      else:
        student.grades[course] = [grade]
    else:
      return 'Ошибка'

  def __str__(self):
    return super().__str__()

def course_avg_grade(students, course):
  for student in students:
    if isinstance(student, Student) and course in student.grades:
      return (
        f'Средняя оценка за домашнее задание по курсу {course}: '
        f'{round(sum(student.grades[course]) / len(student.grades[course]), 1)}'
      )
  return 'У студентов нет оценок за данный курс.'

def lecturer_avg_grade(lecturers, course):
  for lecturer in lecturers:
    if isinstance(lecturer, Lecturer) and course in lecturer.grades:
      return (
        f'Средняя оценка за лекции по курсу {course}: '
        f'{round(sum(lecturer.grades[course]) / len(lecturer.grades[course]), 1)}'
      )
  return 'У лекторов нет оценок за данный курс.'
 
student1 = Student('Top', 'Kekson', 'male')
student1.finished_courses += ['Git']
student1.courses_in_progress += ['C++', 'Python']
student1.grades['Git'] = [8, 7, 10, 9, 7]
student1.grades['Python'] = [6, 7, 8, 10, 10]
student1.grades['C++'] = [10, 10]

student2 = Student('Ushat', 'Pomoev', 'male')
student2.finished_courses += ['C++']
student2.courses_in_progress += ['Python', 'Git']
student2.grades['Git'] = [10, 10, 9, 10]
student2.grades['Python'] = [10, 10, 10, 9]
student2.grades['C++'] = [5, 6, 7, 8, 9]

reviewer1 = Reviewer('Vasily', 'Pupkin')
reviewer1.courses_attached += ['Python', 'Git']

reviewer2 = Reviewer('Hans', 'Bocharov')
reviewer2.courses_attached += ['C++', 'Git']

lecturer1 = Lecturer('Guido', 'van Rossum')
lecturer1.courses_attached += ['Python']
lecturer1.grades['Python'] = [10, 9, 10, 10]

lecturer2 = Lecturer('Bjarne', 'Stroustrup')
lecturer2.courses_attached += ['C++']
lecturer2.grades['C++'] = [10, 10, 10, 9]

student1.rate_lecturer(lecturer2, 'C++', 9)
student2.rate_lecturer(lecturer1, 'Python', 10)

reviewer1.rate_hw(student1, 'Python', 10)
reviewer2.rate_hw(student2, 'Git', 4)

student_lst = [student1, student2]
lecturer_lst = [lecturer1, lecturer2]

print(
  'Студенты:', student1, student2, 'Ревьюеры:', reviewer1, reviewer2, 
  'Лекторы:', lecturer1,lecturer2, student1 > student2,
  lecturer2 > lecturer1, course_avg_grade(student_lst, 'Git'),
  lecturer_avg_grade(lecturer_lst, 'JavaScript'), sep = '\n\n'
  )