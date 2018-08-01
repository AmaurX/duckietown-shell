from abc import ABCMeta, abstractmethod

class DTCommandAbs(object):
    __metaclass__ = ABCMeta

    name = None
    commands = None
    fake = False

    @staticmethod
    @abstractmethod
    def command(shell, word):
        pass

    @staticmethod
    def complete():
        return []

    @staticmethod
    def do_command(cls, shell, line):
        # print '>[%s]@(%s, %s)' % (line, cls.name, cls.__class__)
        line = line.strip()
        parts = [ p.strip() for p in line.split(' ') ]
        word = parts[0]
        # print '[%s, %r]@(%s, %s)' % (word, parts, cls.name, cls.__class__)
        if len(word) > 0:
            if len(cls.commands) > 0:
                if word in cls.commands:
                    cls.commands[word].do_command(cls.commands[word], shell, ' '.join(parts[1:]))
                else:
                    print 'Command `%s` not recognized.\nAvailable sub-commands are:\n\n\t%s' % ( word.strip(), '\n\t'.join(cls.commands.keys()) )
            else:
                cls.command(shell, parts)
        else:
            if len(cls.commands) > 0:
                print 'Available sub-commands are:\n\n\t%s' % '\n\t'.join(cls.commands.keys())
            else:
                if not cls.fake:
                    cls.command(shell, parts)

    @staticmethod
    def complete_command(cls, shell, word, line, start_index, end_index):
        # print '[%s](%s)@(%s, %s)' % (word, line, cls.name, cls.__class__)
        word = word.strip()
        line = line.strip()
        subcmds = cls.commands.keys()
        parts = [ p.strip() for p in line.split(' ') ]
        #
        partial_word = len(word) != 0
        if parts[0] == cls.name:
            if len(parts) == 1 or (len(parts) == 2 and partial_word):
                static_comp = [ k for k in cls.complete() if (not partial_word or k.startswith(word)) ]
                comp_subcmds = static_comp + [ k for k in subcmds if (not partial_word or k.startswith(word)) ]
                # print '!T'
                return comp_subcmds
            if len(parts) > 1 and parts[1] in cls.commands.keys():
                child = parts[1]
                nline = ' '.join(parts[1:])
                # print '!C'
                return DTCommandAbs.complete_command(cls.commands[child], shell, word, nline, start_index, end_index)
        # print '!D'
        return []
