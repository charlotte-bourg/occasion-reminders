function Tier(props) {
    return (
    <tr>
        <td>{props.name}</td>
        <td>{props.description}</td>
        <td>{props.reminder_days_ahead}</td>
        <td>{props.reminder_type}</td>
      </tr>
    );
}

function TiersContainer(){
    const [tiers, setTiers] = React.useState([]);
    
    function addTier(newTier) {
        const currentTiers = [...tiers];
        setTiers([...currentTiers, newTier]);
    }

    React.useEffect(() => {
        fetch('/tiers')
            .then((response) => response.json())
            .then((responseData) => setTiers(responseData))
    }, []);
    const tiersRows = [];
    console.log(tiers)
    for (const tier of tiers) {
        tiersRows.push(
        <Tier
            name={tier.name}
            description={tier.description}
            reminder_days_ahead={tier.reminder_days_ahead}
            reminder_type={tier.reminder_type}
        />,
        );
    }
    return(<React.Fragment>
        <table>{tiersRows}</table>
        </React.Fragment>)
}

//https://dev.to/ondiek/connecting-a-react-frontend-to-a-flask-backend-h1o
ReactDOM.render(<TiersContainer/>, document.querySelector("#tiers"));