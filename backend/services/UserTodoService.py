from asyncpg import exceptions

from sqlmodel import Session

from sqlalchemy import exc

from exceptions.TodoDuplicationException import TodoDuplicationException
from models.Todo import Todo
from request import CreateTodoRequest


# zalozit todo do databaze
# sqlmodel -> session (sqlalchemy orm)
# jak odchytit dataintegrity error/duplication/unique constraint

# potrebuju user_id -> get_current_user pres deps v controlleru
# potrebuju label -> posle mi postman/frontend -> Jdu vytvaret request tridu

# potrebuju vytvorit instanci, pouzit metodu add na session a commitnout to

# Budu vracet data a jake??? -> Ano budu protoze frontend nezna todo_id
# minimalne todo_id -> Pripadne cely objekt
# Je na todo objektu heslo nebo nejaka citliva data?? Ne nejsou -> Takze plati to o radek vys


class UserTodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_todo(self, user_id: int, data: CreateTodoRequest):
        try:
            new_todo = Todo(label=data.label, user_id=user_id)

            self.session.add(new_todo)
            await self.session.commit()

            return new_todo
        except (exc.IntegrityError, exceptions.UniqueViolationError):
            raise TodoDuplicationException(f"Todo [{data.label}] already exists")
        except Exception as e:
            raise Exception(e)
