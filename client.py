import time
from threading import Thread

from UserDialog import UserDialog
from connection import Connection
from whiteboard import WhiteBaord

class Client(Thread,WhiteBaord):

    Objects = {'line': 'L', 'oval': 'O', 'circle': 'C', 'rectangle': 'R', 'square': 'S', 'erase': 'E', 'drag': 'DR'}

    def __init__(self):
        self.conn = Connection()
        Thread.__init__(self)
        WhiteBaord.__init__(self)
        self._init_mouse_event()
        self.setDaemon(True)
        self.isMouseDown = False
        self.x_pos = None
        self.y_pos = None
        self.last_time = None

    def _init_mouse_event(self):
        self.drawing_area.bind("<Motion>",self.motion)
        self.drawing_area.bind("<ButtonPress-1>",self.left_but_down)
        self.drawing_area.bind("<ButtonRelease-1>",self.left_but_up)

    def motion(self,event= None):
        if self.isMouseDown ==True and self.drawing_tool == 'pencil':
            now = time.time()
            if now - self.last_time < 0.02:
                print('too fast')
                return
            self.last_time = now
            msg = ('D',self.x_pos,self.y_pos, event.x, event.y, WhiteBaord.color)
            self.conn.send_message(msg)
            self.x_pos = event.x
            self.y_pos = event.y
        elif self.drawing_tool == 'eraser' and self.isMouseDown == True:
            self.send_del_msg(event)


    def send_del_msg(self,event):
        canvas_item_tuple = self.drawing_area.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        if len(canvas_item_tuple) > 0:
            to_delete_id = max(canvas_item_tuple)
            tags = self.drawing_area.gettags(to_delete_id)
            msgid = tags[0]
            msg = ('Z', msgid)
            self.conn.send_message(msg)


    def left_but_up(self,event=None):
        self.isMouseDown=False
        print(event.x,event.y)
        self.last_time = None
        self.line_x2,self.line_y2=event.x,event.y
        if self.drawing_tool =='text':
            self.draw_text()
        else:
            self.draw_one_obj()

    def draw_text(self):
        text_to_draw = UserDialog._Text
        msg = ('T', self.line_x1, self.line_y1, 'red',text_to_draw)
        self.conn.send_message(msg)

    def draw_one_obj(self):
        tool = self.drawing_tool
        if tool not in Client.Objects.keys():
            return
        else:
            cmd_type = Client.Objects[tool]
            msg = (cmd_type,self.line_x1, self.line_y1, self.line_x2, self.line_y2, WhiteBaord.color)
            self.conn.send_message(msg)

    def left_but_down(self,event=None):
        self.isMouseDown= True
        self.x_pos = event.x
        self.y_pos = event.y
        self.last_time = time.time()
        self.line_x1,self.line_y1 = event.x,event.y

        if self.isMouseDown == True and self.drawing_tool == 'eraser':
            self.send_del_msg(event)

    def run(self):
        while True:
            msg = self.conn.receive_msg()
            # print('clientrecv',msg)
            self.draw_from_msg(msg)
            if msg == 'xxx':
                pass

            # time.sleep(0.1)
if __name__ == '__main__':
    client=Client()
    client.start()
    client.show_window()