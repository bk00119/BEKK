import pytest
from bson.objectid import ObjectId
import db.tasks as tsks
import db.db_connect as dbc
from unittest.mock import patch

@pytest.fixture(scope='function')
def temp_task():
  task = { 
    tsks.USER_ID: "6575033f3b89d2b4f309d7af",
    tsks.GOAL_ID: "65d2dd8abe686c2ec340e298", 
    tsks.CONTENT: "test content",
    tsks.IS_COMPLETED: False
  }
  ret = tsks.add_task(task[tsks.USER_ID], task[tsks.GOAL_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
  task[tsks.ID] = str(ret)
  return task  

@pytest.mark.skip(reason="using local MongoDB") 
def test_get_all_tasks():
  tasks = tsks.get_tasks()
  assert isinstance(tasks, dict)
  assert len(tasks) >= 0
  for task in tasks:
    assert isinstance(task, str)
    assert isinstance(tasks[task], dict)
    assert isinstance(tasks[task]['likes'], list)
 
def test_add_task():
  test_task = tsks.get_new_test_task()
  ret = tsks.add_task(test_task[tsks.USER_ID], test_task[tsks.GOAL_ID], test_task[tsks.CONTENT], test_task[tsks.IS_COMPLETED])
  assert isinstance(ret, str) # return: str(_id)
  tsks.del_task(ret)

def test_del_task(temp_task):
  task = temp_task
  tsks.del_task(ObjectId(task[tsks.ID]))
  assert not tsks.id_exists(ObjectId(task[tsks.ID]))
  
def test_del_task_not_exist():
  id = dbc.gen_object_id()
  with pytest.raises(ValueError):
    tsks.del_task(id)


# adds test task entry and checks if entry has been made via get_task db endpoint 
# deletes test task from database - cleanup
def test_get_task(temp_task):
  ret = tsks.get_task(temp_task[tsks.ID])
  assert isinstance(ret, dict)
  assert str(ret[tsks.USER_ID]) == temp_task[tsks.USER_ID]
  assert str(ret[tsks.GOAL_ID]) == temp_task[tsks.GOAL_ID]
  assert ret[tsks.CONTENT] == temp_task[tsks.CONTENT]
  assert ret[tsks.IS_COMPLETED] == temp_task[tsks.IS_COMPLETED]
  tsks.del_task(temp_task[tsks.ID])


def test_get_tasks(temp_task):
  # create task
  ret = tsks.get_tasks({tsks.ID: ObjectId(temp_task[tsks.ID])})

  for key in ret:
    task = ret[key]
    assert str(task[tsks.USER_ID]) == temp_task[tsks.USER_ID]
    assert str(task[tsks.GOAL_ID]) == temp_task[tsks.GOAL_ID]
    assert task[tsks.CONTENT] == temp_task[tsks.CONTENT]
    assert task[tsks.IS_COMPLETED] == temp_task[tsks.IS_COMPLETED]
    tsks.del_task(key)



def test_get_task_not_exist():
  id = dbc.gen_object_id()
  with pytest.raises(ValueError):
    tsks.get_task(id)

@pytest.mark.skip("pausing task retrieval based on user information")
def test_get_user_tasks(temp_task):
  task = temp_task
  ret = tsks.get_user_tasks(task[tsks.USER_ID])
  print(ret[task[tsks.ID]])
  assert isinstance(ret, dict)
  assert ret[task[tsks.ID]][tsks.USER_ID] == task[tsks.USER_ID]
  assert ret[task[tsks.ID]][tsks.GOAL_ID] == task[tsks.GOAL_ID]
  assert ret[task[tsks.ID]][tsks.CONTENT] == task[tsks.CONTENT]
  assert ret[task[tsks.ID]][tsks.IS_COMPLETED] == task[tsks.IS_COMPLETED]
  tsks.del_task(ObjectId(task[tsks.ID]))

def test_task_like_unlike(temp_task):
  task = temp_task
  user_id = dbc.gen_object_id()
  tsks.like_task(task[tsks.ID], user_id)
  assert tsks.is_task_liked(task[tsks.ID], user_id)
  tsks.unlike_task(task[tsks.ID], user_id)
  assert not tsks.is_task_liked(task[tsks.ID], user_id)
