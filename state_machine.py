from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', None))   # 가상의 START 이벤트 전달

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, event):
        # event 가 어떤 이벤트인지 체크할 수 있어야함.
        for check_event in self.rules[self.cur_state].keys():   # 현재 상태에서 들어올 수 있는 이벤트들
            if check_event(event):    # 이벤트가 발생되었을 때
                self.next_state = self.rules[self.cur_state][check_event]
                self.cur_state.exit(event)   # 현재 상태에서 나감.(해당 이벤트를 던져주기)
                self.next_state.enter(event) # 다음 상태로 들어감.(해당 이벤트를 던져주기)
                # 상태 변환 디버그 프린트
                print(f'State Transition: {self.cur_state.__class__.__name__} - {event_to_string(event)} -> {self.next_state.__class__.__name__}')
                self.cur_state = self.next_state    # 현재 상태 = 다음 상태로 변경!
                return
        # return 되지 않음. 이벤트에 대한 처리가 안됐다... 따라서 문제가 발생했다는 뜻
        print(f'처리되지 않은 이벤트 {event_to_string(event)} 가 있습니다')