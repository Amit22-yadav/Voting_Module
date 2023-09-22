# Sample Hello World Beaker smart contract - the most basic starting point for an Algorand smart contract
import beaker as bk
import pyteal as pt
# from pyteal import Expr, Seq, Assert, Not
from beaker.lib.storage import BoxMapping
# from beaker.lib.storage import BoxList


class Mystate:
    result = bk.GlobalStateValue(pt.TealType.uint64)

class Proposal_Record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    proposal_name:pt.abi.Field[pt.abi.String]
    asset_count:pt.abi.Field[pt.abi.Uint64]
    asset_id:pt.abi.Field[pt.abi.Uint64]
    Amount:pt.abi.Field[pt.abi.Uint64]
    # msg:pt.abi.Field[pt.abi.String]
    descr = "record stored"
    
class User_per_proposal_record(pt.abi.NamedTuple):
    user_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]

class Proposal_Record_State:
    proposal_rec = BoxMapping(pt.abi.String,Proposal_Record)
    user_rec = BoxMapping(pt.abi.String,User_per_proposal_record,prefix=pt.Bytes("_"))



app = bk.Application("Voting_Proposal_4fn",state = Proposal_Record_State())



@app.external
def Register_proposal(proposal_id:pt.abi.String,proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,asset_id:pt.abi.Uint64,Amount:pt.abi.Uint64,* ,output:Proposal_Record) -> pt.Expr:
    
    proposal_store = Proposal_Record()

  
    return pt.Seq(

        proposal_store.set(proposal_id,proposal_name,asset_count,asset_id,Amount),
        pt.Assert(app.state.proposal_rec[proposal_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),
        # output.set(pt.Concat(pt.Bytes("Proposal_id already exists, "))),
        app.state.proposal_rec[proposal_id.get()].set(proposal_store),
        # msg.set(pt.Concat(pt.Bytes("Proposal Registered Successfully "))),
        app.state.proposal_rec[proposal_id.get()].store_into(output),


    )

   
   
@app.external

def Registred_user_per_proposal(user_id:pt.abi.String,token_count:pt.abi.Uint64,*,output:User_per_proposal_record)-> pt.Expr:
    registred_user = User_per_proposal_record()
    return pt.Seq(
    registred_user.set(user_id,token_count),
    pt.Assert(app.state.user_rec[user_id.get()].exists()==pt.Int(0),comment="User_ID already exists"),
    app.state.user_rec[(user_id).get()].set(registred_user),
    # output.set(pt.Concat(pt.Bytes("user Registred Successfully")))
    app.state.user_rec[user_id.get()].store_into(output),
    )

@app.external

def update_proposal(proposal_id:pt.abi.String,proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,asset_id:pt.abi.Uint64,Amount:pt.abi.Uint64,* ,output:Proposal_Record,)-> pt.Expr:
    existing_proposal_store = Proposal_Record()
    update_proposal_store = Proposal_Record()

    return pt.Seq(
        existing_proposal_store.decode(app.state.proposal_rec[proposal_id.get()].get()),
        update_proposal_store.set(proposal_id,proposal_name,asset_count,asset_id,Amount),
        app.state.proposal_rec[proposal_id.get()].set(update_proposal_store),
        app.state.proposal_rec[proposal_id.get()].store_into(output),
        # msg.set(pt.Concat(pt.Bytes("Proposal_updated Successfully")))


    )

@app.external
def Update_Users(user_id:pt.abi.String,token_count:pt.abi.Uint64,*,output:User_per_proposal_record)->pt.Expr:
    existing_user_store = User_per_proposal_record()
    update_user_store = User_per_proposal_record()
    return pt.Seq(
        existing_user_store.decode(app.state.user_rec[user_id.get()].get()),
        update_user_store.set(user_id,token_count),
        app.state.user_rec[user_id.get()].set(update_user_store),
        app.state.user_rec[user_id.get()].store_into(output),


    )

# @app.external
# def Voting_Record(proposal_id:pt.abi.String,user_id:pt.abi.String,*,output:pt.abi.String)-> pt.Expr:


@app.external

def read_proposal_store(proposal_id:pt.abi.String,*,output:Proposal_Record)-> pt.Expr:
    return app.state.proposal_rec[proposal_id.get()].store_into(output)

@app.external

def read_user_proposal_store(user_id:pt.abi.String,*,output:User_per_proposal_record)-> pt.Expr:
    return app.state.user_rec[user_id.get()].store_into(output)





