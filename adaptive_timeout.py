class AdaptiveTimeout:

    def __init__(self):

        self.rtt = 2
        self.alpha = 0.2


    def update(self,sample):

        self.rtt = (
            (1-self.alpha)*self.rtt
            +
            self.alpha*sample
        )


    def get_timeout(self):

        timeout = self.rtt * 5

        return max(
            timeout,
            6
        )