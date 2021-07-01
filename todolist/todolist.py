from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_week_days(today_):
    return [today_ + timedelta(days=i) for i in range(7)]


end = False
while not end:
    today = datetime.now().date()
    all_tasks = session.query(Task).order_by(Task.deadline).all()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

    user = input()
    if user == '0':
        print("\nBye!")
        break

    elif user == '1':
        tt = session.query(Task).filter(Task.deadline == today).all()
        if len(tt) == 0:
            print("")
            print(f"Today {today.day} {today.strftime('%b')}:")
            print("Nothing to do!\n")

        else:
            print("")
            print(f"Today {today.day} {today.strftime('%b')}:")
            for x in tt:
                print(f"{tt.index(x) + 1}. {x}")
            print("")

    elif user == '2':
        print("")
        week_days = get_week_days(today)

        for day in week_days:
            m_day = session.query(Task).filter(Task.deadline == day).all()
            if not m_day:
                print(f"{day.strftime('%A')} {day.strftime('%-d')} {day.strftime('%b')}:")
                print("Nothing to do!")
            else:
                print(f"{day.strftime('%A')} {day.strftime('%-d')} {day.strftime('%b')}:")
                for x in range(len(m_day)):
                    print(f"{m_day.index(m_day[x])+1}. {m_day[x].task}")
            print()

    elif user == '3':
        print("")
        print("All tasks:")
        for x in range(len(all_tasks)):
            task = all_tasks[x]
            print(f"{x+1}. {task.task}. {task.deadline.strftime('%-d')} {task.deadline.strftime('%b')}")
        print("")

    elif user == '4':
        missed_tasks = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()
        print("")
        print("Missed tasks:")
        if not missed_tasks:
            print("Nothing is missed!")
            print("")
        else:
            for task in missed_tasks:
                deadline_s = task.deadline.strftime
                print(f"{missed_tasks.index(task)+1}. {task.task}. {deadline_s('%-d')} {deadline_s('%b')}")
            print("")

    elif user == '5':
        print("")
        task = input("Enter task\n")
        deadline = input("Enter deadline\n")
        new_row = Task(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print("")

    elif user == '6':
        print("")
        if not all_tasks:
            print("Nothing to delete")
            print("")
        else:
            print("Choose the number of the task you want to delete:")
            for task in all_tasks:
                deadline_s = task.deadline.strftime
                print(f"{all_tasks.index(task)+1}. {task.task}. {deadline_s('%-d')} {deadline_s('%b')}")
            delete_t = input()
            session.query(Task).filter(Task.task == all_tasks[int(delete_t) - 1].task).delete()
            session.commit()
            print("The task has been deleted!\n")
            print(all_tasks)
