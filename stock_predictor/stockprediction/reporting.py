import property as p
from property import *

techrep=p.techreport
def create_reportfile(path, header):
    if os.path.exists(path):
        pass
    else:
        f = open(path, mode='w')
        reportcol=','.join(p.reportcol)
        print(reportcol)
        f.writelines(reportcol)
        f.write('\n')
        f.close()

def get_forcasted_dates(dates,days):
    """
    :param dates: last 3 dates from symbol stock data
    :param days:  n,no of days to predict
    :return: n dates
    """

    a,b,c = dates[0],dates[1],dates[2]

    if (b - a) < (c - b):
        if b != a:
            diff = b - a
        else:
            diff = c - b
    elif c != b:
        diff = c - b
    else:
        diff = b - a

    widthdays = diff.days * 24 * 60
    width = (diff.seconds) // 60

    width += widthdays

    startdate=c
    if width==1440:
        ndates=pd.bdate_range(startdate,dtype='datetime64[s]',periods=days+1)

    else:
        print(a,b,c,width)
        ndates=pd.date_range(startdate,dtype='datetime64[s]',freq=pd.DateOffset(minutes=width),periods=(days+1))
    return ndates[1:]

def create_basic_report(report_dict,header):
    ##Sample  header = 'NIFTY-60-RSI10-BBu_10-BBl-BBs-MA20-MA50-MA252-RVR'

    rep_header = (header).split("-")
    report_dict[header] = pd.DataFrame(
        columns=p.reportcol)
    collist=rep_header[2:-1]

    try:
        report_dict[header].set_value(header, 'symbol', rep_header[0])
        report_dict[header].set_value(header, 'Days', rep_header[1])
        report_dict[header].set_value(header, 'model', rep_header[-1])


        while(len(collist)>1):
            if collist[0].startswith('RSI'):
                report_dict[header].set_value(header, 'RSI', collist[0][3:])
                collist.pop(0)
            elif collist[0].startswith('BBu_'):
                report_dict[header].set_value(header, 'BBANDS', collist[0][4:])
                collist.pop(0)
            elif collist[0].startswith('MA'):
                report_dict[header].set_value(header, 'MA1', collist[0][2:])
                collist.pop(0)
                try:
                    if collist[0].startswith('MA'):
                        report_dict[header].set_value(header, 'MA2', collist[0][2:])
                        collist.pop(0)
                    if collist[0].startswith('MA'):
                        report_dict[header].set_value(header, 'MA3', collist[0][2:])
                        collist.pop(0)
                    if collist[0].startswith('MA'):
                        report_dict[header].set_value(header, 'MA4', collist[0][2:])
                        collist.pop(0)
                except IndexError as e:
                    pass
            else:
                collist.pop(0)


    except IndexError as e:
        pass
    except Exception as e:
        print('basicreporting error',e)
    finally:
        return report_dict


def create_report(report_dict,header,x,y):
    try:
        report_dict[header].set_value(header, str(x),y)
    except Exception as e:
        print('reporting error', e)
    finally:
        return report_dict

def mod_report(old=reportpath,new=mod_reportpath):
    if os.path.exists(old):
        df = pd.read_csv(old)
    else:
        print(old,' does not exist')
        print('reading last run file')
        df = pd.read_csv(techrep)   # if technical file for the current day do not exist then read last run technical file.
    df=df.drop_duplicates()
    print(__name__,"mod_report1",df)
    mod_df=df.loc[df.groupby(['symbol', 'Days'])['RMSE'].idxmin()]
    mod_df = df.sort_values("RMSE")   #Sort DF with least values.
    mod_df.to_csv(new,index=False)
    return mod_df



