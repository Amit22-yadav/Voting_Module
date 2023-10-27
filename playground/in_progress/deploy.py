from demo import(
    app,
    Register_proposal
)
from beaker import localnet, client
from beaker.consts import algo
from algokit_utils.logic_error import LogicError
app.build().export("./artifacts")

accounts = localnet.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=localnet.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_client.create()

app_client.fund(1 * algo)
app_client.call(
    Register_proposal,
     proposal_id="5",
     proposal_name="ada",
     asset_count=123,
     asset_id=433434,
     Amount=434,
    boxes=[(app_client.app_id, "5")],
)
try:
    value = app_client.call(
        Register_proposal,  proposal_id="5",proposal_name="ada",
     asset_count=123,
     asset_id=433434,
     Amount=434,boxes=[(app_client.app_id, "1")]
    )
    print(value.return_value)
except LogicError as e:
    print("Not created succesfully")
