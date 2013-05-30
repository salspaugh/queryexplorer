
import matplotlib.pyplot as plt
import numpy as np
from queryexplorer import connect_db

SPECIAL_ARGS = "/Users/salspaugh/queryexplorer/data.storm/args/plottable_args_template_cnts_user_cnts.csv"
ROWS = 15
COLS = 10

class Context(object):      # of argument foo

    def __init__(self, arg):
        
        self.arg = arg
        
        self.grp_filtered_on_as_value = 0  # SEARCH =foo
        self.grp_filtered_on_as_field = 0  # SEARCH foo=
        self.grp_argument_to_top = 0             # TOP foo
        self.grp_projected = 0          # FIELDS(PLUS) foo TABLE foo
        self.grp_unprojected = 0        # FIELDS(MINUS) foo
        self.grp_grouped_by = 0         # by foo
        self.grp_argument_renamed_as = 0         # as foo
        self.grp_field_extracted_to = 0       # REGEX foo=
        self.grp_argument_to_aggregation = 0         # STATS(COUNT) foo
        self.grp_argument_to_arithmetic_transformation = 0         # EVAL, STATS
        self.grp_field_used_in_conditional = 0
        self.grp_argument_to_option = 0
        self.grp_sorted_by = 0
        self.grp_value_used_in_other_transformation = 0
        self.grp_field_used_in_other_transformation = 0
        self.grp_field_used_as_function_domain = 0

        self.contexts = sorted(filter(lambda x: x[0:4] == "grp_", self.__dict__.keys()))
        self.colors = [
                        "#843c39", # dark red
                        "#b5cf6b", # light green
                        "#5254a3", # dark purple-blue
                        "#de9ed6", # light pink
                        "#637939", # dark green 
                        "#9c9ede", # light purple
                        "#8c6d31", # dark yellow
                        "#d6616b", # light red
                        "#7b4173", # dark purple-red
                        "#e7ba52", # light yellow
                        "#a55194", # dark pink
                        "#8ca252", # green
                        "#6b6ecf", # purple
                        "#bd9e39", # yellow
                        "#ce6dbd", # pink
                        "#cedb9c", # lighter green
                        #"#e7cb94", # lighter yellow
                        #"#e7969c", # lighter red
                        #"#ad494a", # red
                    ]
    
    def __lt__(self, other):
        return ([getattr(self, attr) for attr in self.contexts] < [getattr(other, attr) for attr in other.contexts])

    def __eq__(self, other):
        return ([getattr(self, attr) for attr in self.contexts] == [getattr(other, attr) for attr in other.contexts])

    def nothing_set(self):
        for attr in self.contexts:
            if getattr(self, attr):
                return False
        return True
    
    def number_set(self):
        return sum([getattr(self, attr) for attr in self.contexts])

    def get_counts(self):
        return [getattr(self, attr) for attr in self.contexts]

    def get_labels(self):
        return [s.replace("grp_", "").replace("_", " ") for s in self.contexts]

    def get_colors(self):
        return self.colors

def read_special_args():
    args = {}
    with open(SPECIAL_ARGS) as special_args:
        for line in special_args.readlines():
            line = line.strip()
            if line == "":
                continue
            if line.find("#") > -1:
                continue
            parts = line.split(',')
            raw = parts[2]
            converted = raw.strip('"').lower()
            if converted in ["get", "head", "post"]:
                converted = "get|head|post"
            if converted[0:5] == "date_":
                converted = "date_*"
            if converted[0:4] == "fail":
                converted = "fail"
            if converted in ["true", "false"]:
                converted = "true|false"
            if converted.find("/var/log") == 0:
                converted = "/var/log/*"
            if converted.find("login") > -1:
                converted = "login"
            if converted.find("access") > -1:
                converted = "access_*"
            if not converted in args:
                args[converted] = []
            args[converted].append(raw)
    print "Number of args:", len(args)
    labels = []
    for (label, placement) in labeling():
        rawlist = args[label]
        labels.append(((label, placement), rawlist))
    return labels

def extract_context(cleanarg, rawlist):
    c = Context(cleanarg)
    db = connect_db()
    number_commands = 0
    print
    for arg in rawlist:
        print "arg: ", arg
        cursor = db.execute("SELECT command, text FROM queries, commands, args \
                                WHERE queries.id = args.query_id \
                                AND args.command_id = commands.id \
                                AND arg=?", [arg])
        for (command, query) in cursor.fetchall():
            print "\tcmd:", command

            number_commands += 1
            set = False
            set_field = False
            if command.find("SEARCH") == 0 or command.find("WHERE") == 0:
                for comparator in ["=", ">", "<", "!=", "=="]:
                    if query.find(arg + comparator) > -1 or query.find(arg + " " + comparator) > -1:
                        c.grp_filtered_on_as_field += 1
                        set = True
                        set_field = True
                if not set_field:        
                    c.grp_filtered_on_as_value += 1
                    set = True

            if command.find("DEDUP") == 0:
                c.grp_filtered_on_as_field += 1
                set = True

            if command.find("TOP") == 0:
                try:
                    int(c.arg)
                    c.grp_argument_to_option += 1
                except:
                    c.grp_argument_to_top += 1
                    set = True

            if command.find("SORT") == 0:
                try:
                    int(c.arg)
                    c.grp_argument_to_option += 1
                except:
                    if query.find("=" + arg) == -1:
                        c.grp_sorted_by += 1
                        set = True

            if command.find("FIELDS(PLUS)") == 0 or command.find("TABLE") == 0 or command.find("EXPORT") == 0:
                c.grp_projected += 1
                set = True

            if command.find("FIELDS(MINUS)") == 0:
                c.grp_unprojected += 1
                set = True

            if command.find("INPUTLOOKUP") == 0 or command.find("ABSTRACT") == 0:
                if query.find("=" + arg) > -1:
                    c.grp_argument_to_option += 1
                    set = True

            if command.find("HEAD") == 0:
                c.grp_argument_to_option += 1
                set = True

            if command.find("STATS") == 0 or command.find("TIMECHART") == 0 or command.find("CHART") == 0:
                for function in ["count", "min", "avg", "max", "sum", "c", "values", "range", "last", "distinct_count", "dc"]:
                    if query.find(function + " " + arg) > -1 or query.find(function + "(" + arg + ")") > -1 or query.find(function + " (" + arg + ")") > -1:
                        c.grp_argument_to_aggregation += 1
                        set = True
            
            if (command.find("STATS") == 0 or command.find("EVAL") == 0 or command.find("CHART") == 0 or command.find("TIMECHART") == 0) and command.find("AS") > -1:
                if query.find("as " + arg) > -1 or query.find("AS " + arg) > -1:
                    c.grp_argument_renamed_as += 1
                    set = True
            
            if (command.find("STATS") == 0 or command.find("EVAL") == 0 or command.find("CHART") == 0 or command.find("TIMECHART") == 0) and command.find("OVER") > -1:
                if query.find("over " + arg) > -1 or query.find("OVER " + arg) > -1:
                    c.grp_field_used_as_function_domain += 1
                    set = True

            if (command.find("STATS") == 0 or command.find("EVAL") == 0 or command.find("CHART") == 0 or command.find("TIMECHART") == 0) and command.find("BY") > -1:
                if query.find("by " + arg) > -1 or query.find("BY " + arg) > -1 or query.find("by") < query.rfind(arg):
                    c.grp_grouped_by += 1
                    set = True

            if command.find("EVAL") > -1 and (command.find("DIVIDES") > -1 or command.find("TIMES") > -1 or command.find("PLUS") > -1):
                c.grp_argument_to_arithmetic_transformation += 1
                set = True

            if command.find("EVAL") > -1:
                if query.find(arg + "=") > -1:
                    c.grp_field_used_in_conditional += 1
                    set = True
                else:
                    c.grp_value_used_in_other_transformation += 1
                    print command
                    set = True

            if command.find("MULTIKV") == 0 or command.find("CONVERT") == 0 or command.find("BUCKET") == 0 or command.find("REX") == 0 or command.find("REPLACE") == 0 or command.find("REGEX") == 0:
                c.grp_field_used_in_other_transformation += 1
                print command
                set = True

            if arg == "false" and not set:
                c.grp_argument_to_option += 1

            if not set:
                print "\t\t\tNo case for this one!"
    
    db.close()
    if c.number_set() < number_commands: 
        print "Missed a case!", arg
        exit()
    return c

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom', size='x-large')

def append_plot(context, i):
    #plt.subplot(ROWS, COLS, i)
    width = 1.0
    counts = context.get_counts()
    s = sum(counts)
    counts = [float(c)/float(s) for c in counts]
    labels = context.get_labels()
    colors = context.get_colors()
    lefts = np.cumsum(counts)
    lefts = np.insert(lefts, 0, 0)[:-1]
    bottoms = np.array([i]*len(counts))
    print context.arg
    print "\tcounts", counts
    print "\tlefts", len(lefts), lefts
    bars = plt.bar(left=lefts, height=1.0, width=counts, bottom=bottoms, 
                    color=colors, orientation="horizontal", label=labels)

    #bars = plt.bar(ind, counts, width, alpha=0.75, color=colors)
    #plt.xticks([i+width/2 for i in ind], [""]*len(counts))
    #plt.ylim([0,529]) # highest count
    plt.xticks([])
    #plt.title(context.arg, size="x-large")
    #plt.grid(True) 
    return bars

def labeling():
    return [
           #("type",        1),
           #("t",           2),
           #("key",         3),
           #("value",       4),
           #("true|false",  5),
           #("*",           6),
           #("index",       7),
           #("source",      8),
           #("event",       9),
           #("_raw",        10),

           #("0",           11),
           #("1",           12),
           #("10",          13),
           #("100",         14),
           #("1000",        15),
           #("10000",       16),
           #("60",          17),
           #("1024",        18),

           #("2",           21),
           #("3",           22),
           #("4",           23),
           #("5",           24),
           #("6",           25),
           #("7",           26),
           #("15",          27),
           #("20",          28),
           #("50",          29),

           ("200",         31),
          #("200",         31),
          #("301",         32),
          #("302",         33),
          #("304",         34),
          #("400",         35),
          #("401",         36),
          #("403",         37),
           ("404",         38),
          #("499",         39),
          #("500",         40),

          #("info",        41),
          #("debug",       42),
          #("warn",        43),
          #("warning",     44),
          #("exception",   45),
          #("critical",    46),
          #("severe",      47),
          #("error",       48),
          #("fail",        49),
          #("other",       50),
          #
          #("node",        51),
          #("router",      52),
          #("app",         53),
          #("backup",      54),
          #("dev",         55),
          #("out",         56),
          #("prod",        57),
          #("web",         58),
          #("email",       59),
          #("worker",      60),
          #
          #("/var/log/*",  61),
          #("sshd",        62),
          #("syslog",      63),
          #("root",        64),
          #("queue",       65),
          #("env",         66),
          #("title",       67),
          ("metric",      68),
          ("module",      69),
          #("application", 70),

           ("access_*",        71),
           ("get|head|post",   72),
           ("login",	        73),
          #("connection",	    74),
          #("session",	        75),
           ("useragent",	    76),
           ("method",	        77),
          #("referer_domain",  78),
          #("url",	            79),
          #("cookie",	        80),

          #("denied",      81),
          #("refused",     82),
          #("purchase",	83),
          #("account",	    84),
          #("referer",	    85),
          #("click",       86),
          #("activity",    87),
           ("uri",	        88),
          #("uri_domain",	89),
          #("uri_path",	90),
          #
          #("client",	    91),
          #("client_ip",	92),
          #("clientip",	93),
          #("ip",	        94),
          ("user",	    95),
          #("user_id",	    96),
          #("userid",	    97),
          #("uid",	        98),
          #("screen_name",	99),
          #("name",	    100),
          #
           ("status",      101),
          #("level",       102),
          #("severity",    103),
          #("total",       104),
          #("amount",      105),
          #("size",        106),
          #("measurement", 107),
          #("linecount",   108),
          #("count",       109),
          #("bytes",       110),
          #
          #("password",    111),
          ("memory",      112),
          #("group",       113),
          #("process",     114),
          #("pid",         115),
          #("priority",    116),
          #("code",        117),
          #("desc",        118),
          #("msg",         119),
          #("message",     120),
          #
          #("channel",     121),
          #("controller",  122),
          #("cmd",         123),
          #("command",     124),
          #("action",      125),
          #("reason",      126),
          #("host",        127),
          #("path",        128),
          ("device",      129),
          #("device_type", 130),
          #
           ("_time",	    131),
          #("timeout",	    132),
          #("timestamp",	133),
          #("timestartpos",134),
          #("timeendpos",	135),
          #("req_time",	136),
          #("time",	    137),
          #("time_taken",	138),
          #("duration",    139),

          #("id",              141),
          #("server",          142),
          #("eventtype",       143),
          #("splunk_server",   144),
          #("punct",           144),
          #("act",             145),
          #("src",             146),
          #("date",            147),
          #("date_*",          148),
          #("href",            149),
          #("proto",           150),
    ]

def main():
    special_args = read_special_args()
    contexts = []
    print len(special_args)
    last_place = 1
    for ((label, placement), arglist) in special_args:
        if placement == -1:
            placement = last_place + 1
        last_place = placement
        contexts.append(extract_context(label, arglist))
    placement = 1
    contexts = sorted(contexts)
    for context in contexts:
        bars = append_plot(context, placement)
        placement += 1
    ticks = np.arange(len(contexts)) + 1.5
    print ticks
    plt.yticks(ticks, [context.arg for context in contexts], size="x-large")
    plt.figlegend(bars, context.get_labels(), "right")
    plt.show()

main()
