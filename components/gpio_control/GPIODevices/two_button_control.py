try:
    from simple_button import SimpleButton, print_edge_key, print_pull_up_down
except ImportError:
    from .simple_button import SimpleButton, print_edge_key, print_pull_up_down
from RPi import GPIO
import logging
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)


def functionCallTwoButtons(btn1, btn2, functionCall1, functionCall2, functionCallBothPressed=None):
    def functionCallTwoButtons(*args):
        btn1_pin = btn1.pin
        btn2_pin = btn2.pin
        pressed_button = None
        if len(args) > 0 and args[0] in (btn1_pin, btn2_pin):
            logger.debug('Remove pin argument by TwoButtonCallbackFunctionHandler - args before: {}'.format(args))
            pressed_button = args[0]
            args = args[1:]
            logger.debug('args after: {}'.format(args))
        btn1_pressed = btn1.is_pressed
        btn2_pressed = btn2.is_pressed
        logger.info('Btn1 {}, Btn2 {}-args:{}'.format(btn1_pressed, btn2_pressed, args))
        if btn1_pressed and btn2_pressed:
            logger.debug("Both buttons was pressed")
            if functionCallBothPressed is not None:
                logger.debug("Both Btns are pressed, action: functionCallBothPressed")
                logger.info('functionCallBoth')
                return functionCallBothPressed(*args)
            logger.debug('No two button pressed action defined')
        elif btn1_pressed:
            logger.debug("Btn1 is pressed, secondary Btn not pressed, action: functionCall1")
            logger.info('functionCall1')
            return functionCall1(*args)
        elif btn2_pressed:
            logger.debug("Btn2 is pressed, action: functionCall2")
            logger.info('functionCall2')
            return functionCall2(*args)
        elif pressed_button == btn1_pin:
            logger.debug("No Button recognized, called by {}-pin1:functionCall1".format(args))
            logger.info('functionCall1')
            return functionCall1(*args)
        elif pressed_button == btn2_pin:
            logger.debug("No Button recognized, called by {}-pin2:functionCall2".format(args))
            logger.info('functionCall2')
            return functionCall2(*args)
        else:
            logger.debug("No Button recognized, cannot evaluate reason for function call - {}".format(args))
            return None

    return functionCallTwoButtons


class TwoButtonControl:
    def __init__(self,
                 bcmPin1,
                 bcmPin2,
                 functionCallBtn1,
                 functionCallBtn2,
                 functionCallTwoBtns=None,
                 pull_up_down='pull_up',
                 hold_mode=None,
                 hold_time=0.3,
                 bouncetime=500,
                 antibouncehack=False,
                 edge='falling',
                 name='TwoButtonControl'):
        self.bcmPin1 = bcmPin1
        self.bcmPin2 = bcmPin2
        self.functionCallBtn1 = functionCallBtn1
        self.functionCallBtn2 = functionCallBtn2
        self.functionCallTwoBtns = functionCallTwoBtns
        self.pull_up_down = pull_up_down
        self.hold_mode = hold_mode
        self.hold_time = hold_time
        self.bouncetime = bouncetime
        self.antibouncehack = antibouncehack
        self.edge = edge
        self.btn1 = SimpleButton(
            pin=bcmPin1,
            name=name + 'Btn1',
            bouncetime=bouncetime,
            antibouncehack=antibouncehack,
            edge=edge,
            hold_time=hold_time,
            hold_mode=hold_mode,
            pull_up_down=pull_up_down)
        self.btn1.callback_with_pin_argument = True

        self.btn2 = SimpleButton(pin=bcmPin2,
                                 name=name + 'Btn2',
                                 bouncetime=bouncetime,
                                 antibouncehack=antibouncehack,
                                 edge=edge,
                                 hold_time=hold_time,
                                 hold_mode=hold_mode,
                                 pull_up_down=pull_up_down)
        self.btn2.callback_with_pin_argument = True
        generatedTwoButtonFunctionCall = functionCallTwoButtons(self.btn1,
                                                                self.btn2,
                                                                self.functionCallBtn1,
                                                                self.functionCallBtn2,
                                                                self.functionCallTwoBtns
                                                                )
        self.action = generatedTwoButtonFunctionCall
        logger.info('adding new action')
        self.btn1.when_pressed = generatedTwoButtonFunctionCall
        self.btn2.when_pressed = generatedTwoButtonFunctionCall
        self.name = name

    def __repr__(self):
        two_btns_action = self.functionCallTwoBtns is not None
        return '<TwoBtnControl-{}({}, {},two_buttons_action={},hold_mode={},hold_time={},edge={},bouncetime={},antibouncehack={},pull_up_down={})>'.format(
            self.name, self.bcmPin1, self.bcmPin2, two_btns_action,
            self.hold_mode, self.hold_time, print_edge_key(self.edge),
            self.bouncetime, self.antibouncehack,
            print_pull_up_down(self.pull_up_down)
        )


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    pin1 = int(input('please enter first pin'))
    pin2 = int(input('please enter second pin'))
    func1 = lambda *args: print('Function Btn1 executed with {}'.format(args))
    func2 = lambda *args: print('Function Btn2 executed with {}'.format(args))
    func3 = lambda *args: print('Function BothBtns executed with {}'.format(args))
    two_btn_control = TwoButtonControl(pin1, pin2, func1, func2, func3)

    print('running')
    while True:
        pass
