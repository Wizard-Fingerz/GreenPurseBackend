from django.db.models import Sum


class SummaryByAccount:
    def __init__(self, account, total_inflow, total_outflow, balance):
        self.account = account
        self.total_inflow = total_inflow
        self.total_outflow = total_outflow
        self.balance = balance

    @classmethod
    def fromTransactions(cls, transactions):
        accounts = []
        summary = []
        for t in transactions:
            if t.account not in accounts:
                accounts.append(t.account)
        for account in accounts:
            transactions_by_account = transactions.filter(account=account)
            inflow = transactions_by_account.filter(type="inflow").aggregate(
                Sum("amount")
            )
            outflow = transactions_by_account.filter(type="outflow").aggregate(
                Sum("amount")
            )
            if inflow["amount__sum"] is not None:
                total_inflow = inflow["amount__sum"]
            else:
                total_inflow = 0
            if outflow["amount__sum"] is not None:
                total_outflow = outflow["amount__sum"]
            else:
                total_outflow = 0
            balance = total_inflow + total_outflow
            account_summary = cls(account, total_inflow, total_outflow, balance)
            summary.append(account_summary)
        return summary


class SummaryByCategory:
    def __init__(self, inflow, outflow):
        self.inflow = inflow
        self.outflow = outflow

    @classmethod
    def fromTransactions(cls, transactions):
        inflow = {}
        outflow = {}
        categories = []
        inflow_t = transactions.filter(type="inflow")
        outflow_t = transactions.filter(type="outflow")
        for t in transactions:
            if t.type == "inflow" and t.category not in categories:
                total_inflow = inflow_t.filter(category=t.category).aggregate(
                    Sum("amount")
                )
                if total_inflow is not None:
                    inflow[t.category] = total_inflow["amount__sum"]
                else:
                    inflow[t.category] = 0
                categories.append(t.category)
            if t.type == "outflow" and t.category not in categories:
                total_outflow = outflow_t.filter(category=t.category).aggregate(
                    Sum("amount")
                )
                if total_outflow is not None:
                    outflow[t.category] = total_outflow["amount__sum"]
                else:
                    outflow[t.category] = 0
                categories.append(t.category)
        return cls(inflow, outflow)