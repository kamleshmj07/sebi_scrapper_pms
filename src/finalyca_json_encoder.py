import flask
import datetime
import decimal

class FinalycaJSONEncoder(flask.json.JSONEncoder):
    '''
    Used to provide json conversion based on Finalyca requirements
    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%d %b %Y') if obj else None

        elif isinstance(obj, datetime.date):
            return obj.strftime('%d %b %Y') if obj else None

        elif isinstance(obj, float):
            return float(round(obj, 2)) if obj else None

        elif isinstance(obj, decimal.Decimal):
            return float(round(obj, 2)) if obj else None

        else:
            return super().default(obj)
