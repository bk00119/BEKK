import pytest
from bson.objectid import ObjectId
import db.tasks as tsks
import db.db_connect as dbc


@pytest.fixture(scope='function')
def temp_task():
  task = {}
  task[tsks.USER_ID] = "6575033f3b89d2b4f309d7af"
  task[tsks.CONTENT] = "test content"
  task[tsks.GOAL_ID] = "65d2dd8abe686c2ec340e298"
  task[tsks.IS_COMPLETED] = False
  ret = tsks.add_task(task[tsks.USER_ID], task[tsks.GOAL_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
  task[tsks.ID] = ret
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

def test_get_task(temp_task):
  tsks.add_task()
  task = temp_task
  ret = tsks.get_task(ObjectId(task[tsks.ID]))
  assert isinstance(ret, dict)
  assert ret[tsks.USER_ID] == task[tsks.USER_ID]
  assert ret[tsks.GOAL_ID] == task[tsks.GOAL_ID]
  assert ret[tsks.CONTENT] == task[tsks.CONTENT]
  assert ret[tsks.IS_COMPLETED] == task[tsks.IS_COMPLETED]
  tsks.del_task(ObjectId(task[tsks.ID]))


def test_get_task(temp_task):
  # create task
  task = temp_task 
  task_id = task[tsks.ID] # objectID type

  # get task 
  ret = tsks.get_tasks({tsks.ID: task_id})
  assert ret is not None

  # delete task 
  tsks.del_task(task[tsks.ID])





def test_get_task_not_exist():
  id = dbc.gen_object_id()
  with pytest.raises(ValueError):
    tsks.get_task(id)

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
