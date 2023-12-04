import pytest
from bson.objectid import ObjectId
import db.tasks as tsks
import db.db_connect as dbc

@pytest.fixture(scope='function')
def temp_task():
  task = {}
  task[tsks.USER_ID] = "testuser123"
  task[tsks.TITLE] = "test title"
  task[tsks.CONTENT] = "test content"
  task[tsks.STATUS] = 1
  task[tsks.LIKES] = []
  ret = tsks.add_task(task[tsks.USER_ID], task[tsks.TITLE], task[tsks.CONTENT])
  task[tsks.ID] = ret
  return task  

# @pytest.mark.skip(reason="using local MongoDB") 
def test_get_all_tasks():
  tasks = tsks.get_tasks()
  assert isinstance(tasks, dict)
  assert len(tasks) > 0
  for task in tasks:
    assert isinstance(task, str)
    assert isinstance(tasks[task], dict)
    assert isinstance(tasks[task]['likes'], list)
 
def test_add_task():
  test_task = tsks.get_new_test_task()
  ret = tsks.add_task(test_task[tsks.USER_ID], test_task[tsks.TITLE], test_task[tsks.CONTENT])
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
