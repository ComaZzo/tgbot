import optparse


class Config:
    TOKEN: str = ""

    @classmethod
    def read_opts(cls):
        opt = optparse.OptionParser()
        opt.add_option("-t", "--token", dest="token", default="")

        (opts, args) = opt.parse_args()
        cls.TOKEN = opts.token