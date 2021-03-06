from django.contrib import admin

from decimal import Decimal

from models import Wallet, Address, Transaction, OutgoingTransaction


class WalletAdmin(admin.ModelAdmin):
    readonly_fields = [
        'path',
        'change_wallet',
        'getBalanceInfo',
        'listTransactions',
    ]
    exclude = [
        'extra_balance',
    ]

    def listTransactions(self, instance):
        txs = Transaction.objects.filter(wallet=instance).order_by('created_at')
        result = ''
        for tx in txs:
            result += str(tx.created_at) + ' ' + unicode(tx) + '\n'
        return result
    listTransactions.short_description = 'Transactions'

    def getBalanceInfo(self, instance):
        total_balance = instance.getBalance(0)
        result = 'Real Bitcoins: ' + ('%.8f' % (total_balance - instance.extra_balance)) + '\n'
        result += 'Received/send: ' + ('%.8f' % instance.extra_balance) + '\n'
        result += 'Total: ' + ('%.8f' % total_balance) + '\n'
        return result

    getBalanceInfo.short_description = 'Balance'


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = [
        'wallet',
        'subpath_number',
        'address',
    ]


class OutgoingTransactionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
        'inputs_selected_at',
        'sent_at',
        'listInputs',
        'listOutputs',
        'getFee',
    ]

    def listInputs(self, instance):
        if instance.inputs.count() == 0:
            return 'No inputs'
        result = ''
        total = Decimal(0)
        for inpt in instance.inputs.all():
            result += unicode(inpt) + '\n'
            total += inpt.amount
        result += 'Total: ' + str(total) + ' BTC\n'
        return result
    listInputs.short_description = 'Inputs'

    def listOutputs(self, instance):
        if instance.outputs.count() == 0:
            return 'No outputs'
        result = ''
        total = Decimal(0)
        for output in instance.outputs.all():
            result += unicode(output) + '\n'
            total += output.amount
        result += 'Total: ' + str(total) + ' BTC\n'
        return result
    listOutputs.short_description = 'Outputs'

    def getFee(self, instance):
        return instance.calculateFee()
    getFee.short_description = 'Fee'

admin.site.register(Wallet, WalletAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OutgoingTransaction, OutgoingTransactionAdmin)
