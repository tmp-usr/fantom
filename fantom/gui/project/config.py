from ConfigParser import SafeConfigParser


class Config():

    def __init__(self,config_file=''):
        self.parser=SafeConfigParser()
        self.parser.read(config_file)
        self.configFile=config_file
        
    def setParam(self,section, **options):
        for param, value in options.iteritems():
            self.parser.set(section,param,value)
        with open(self.configFile,'wa') as fConfig:
            self.parser.write(fConfig)

    def getParam(self,section, *params):
        for p in params:
            value=self.parser.get(section,p)
            yield value

    def getParams(self,section):
        ''' returns a generator object of a parameter-value pairs in a tuple'''
        params=self.parser.options(section)
        for p in params:
            value=self.parser.get(section,p)
            yield p,value

       




#=cfg.getParam('fastqp','output','i')
#cfg.setParam('fastqp', **{'right':'30','i':'adem.fastq'})
#str=cfg.getCmdString('fastqp','python','fastqp')
#run_cmd(str)

