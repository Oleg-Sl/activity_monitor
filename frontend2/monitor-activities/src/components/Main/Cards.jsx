import React from "react";
import Card from "./Card.jsx";
import Add from "./Add.jsx";
import ClassNames from "classnames";


class Cards extends React.PureComponent {
  state = {
    openCards: true,
    collapsedCards: new Set()
  };

  containerRef = React.createRef();
  cardsContainerRef = React.createRef();

  componentDidMount() {
    // this.checkAfterRender();
    this.checkCardsVisibility();
    // window.addEventListener('resize', this.handleResize);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.data !== this.props.data) {
      // this.checkAfterRender();
      this.checkCardsVisibility();
    }
  }

  checkAfterRender = () => {
    requestAnimationFrame(() => {
      if (this.state.openCards) {
        this.checkCardsVisibility();
      }
    });
  };

  // componentDidMount() {
  //   this.checkCardsVisibility();
  //   window.addEventListener('resize', this.handleResize);
  // }

  // componentDidUpdate(prevProps) {
  //   if (prevProps.data !== this.props.data || prevProps.openCards !== this.props.openCards) {
  //     this.checkCardsVisibility();
  //   }
  // }

  // componentWillUnmount() {
  //   window.removeEventListener('resize', this.handleResize);
  // }

  handleResize = () => {
    clearTimeout(this.resizeTimeout);
    this.resizeTimeout = setTimeout(this.checkCardsVisibility, 100);
  };

  checkCardsVisibility = () => {
    console.log('checkCardsVisibility');
    if (!this.state.openCards || !this.containerRef.current || !this.cardsContainerRef.current) {
      return;
    }

    const container = this.containerRef.current;
    const cardsContainer = this.cardsContainerRef.current;
    const cards = Array.from(cardsContainer.querySelectorAll('.card'));
    const collapsedCards = new Set();
    console.log('cards = ', cards);

    const containerHeight = container.clientHeight;
    const headerHeight = container.querySelector('.card-wrapper__header').clientHeight;
    const availableHeight = containerHeight - headerHeight - 30;
    let usedHeight = 0;
    console.log('availableHeight = ', availableHeight);

    cards.forEach(card => {
      const cardId = card.dataset.id;
      const cardHeader = card.querySelector('.card__header');
      const cardHeaderHeight = cardHeader.clientHeight;
      const cardFullHeight = card.clientHeight;
      console.log('availableusedHeightHeight = ', usedHeight);

      if (usedHeight + cardFullHeight <= availableHeight) {
        usedHeight += cardFullHeight;
      } else {
        collapsedCards.add(cardId);
        usedHeight += cardHeaderHeight;
      }
    });

    this.setState({ collapsedCards });
  };

  handleToggle = () => {
    this.setState(prevState => ({ openCards: !prevState.openCards }), () => {
      if (this.state.openCards) {
        this.checkCardsVisibility();
      }
    });
  };

  get cardsContainer() {
    const { openCards } = this.state;
    
    if (!openCards) {
      return null;
    }

    return (
      <div className="cards" ref={this.cardsContainerRef}>
        {this.cardsList}
      </div>
    );
  }

  get cardsList() {
    const { data } = this.props;
    const { collapsedCards } = this.state;
    
    for (let item of data) {
      if (!item.image) {
        collapsedCards.add(item.id.toString())
      }
    }

    return data.map(item => (
      <Card 
        key={item.id} 
        data={item} 
        collapsed={collapsedCards.has(item.id.toString())}
      />
    ));
  }

  render() {
    // console.log('this.props = ', this.props);
    // console.log('this.state = ', this.state);
    const { name, style, data } = this.props;
    const { openCards } = this.state;
    
    const classes = ClassNames({
      "card-wrapper": true
    });
    
    const styleClass = ClassNames(style);
    
    return (
      <div
        ref={this.containerRef}
        className={`${styleClass} ${classes}`}
      >
        <div className="card-wrapper__header">
          <div className="backlog-name">{name}({data.length})</div>
          <div onClick={this.handleToggle} className="backlog-dots">
            <i className="material-icons">
              {openCards ? "expand_more" : "chevron_right"}
            </i>
          </div>
        </div>
        {this.cardsContainer}
      </div>
    );
  }
}

// class Cards extends React.PureComponent {
//   state = {
//     openCards: true
//   };

//   render() {
//     const { openCards } = this.state;
//     const {
//       name,
//       style,
//       forDragOver,
//       forDrop,
//       onDragEnter,
//       onDragLeave,
//       dropping
//     } = this.props;
//     const classes = ClassNames({
//       "card-wrapper": true,
//       "cards-dropping": dropping
//     });
//     const styleClass = ClassNames(style);
//     return (
//       <div
//         className={styleClass + " " + classes}
//         onDragOver={forDragOver}
//         onDrop={forDrop}
//         onDragEnter={onDragEnter}
//         onDragLeave={onDragLeave}
//       >
//         <div className="card-wrapper__header">
//           <div className="backlog-name">{name}</div>
//           <div onClick={this.handleToggle} className="backlog-dots">
//             <i className="material-icons">
//               {openCards ? "expand_more" : "chevron_right"}
//             </i>
//           </div>
//         </div>
//         {this.cardsContainer}
//       </div>
//     );
//   }

//   handleToggle = () => {
//     return this.setState(prevState => {
//       return { openCards: !prevState.openCards };
//     });
//   };

//   get cardsContainer() {
//     const { type } = this.props;
//     const { openCards } = this.state;
//     if (!openCards) {
//       return null;
//     }
//     return (
//       <div className="cards">
//         {this.cardsList}
//         {/* <Add typeCards={type} /> */}
//       </div>
//     );
//   }

//   get cardsList() {
//     const { data } = this.props;
//     return data.map(item => (
//       <React.Fragment key={item.id}>
//         <Card data={item} />
//       </React.Fragment>
//     ));
//   }
// }

// export default connect(
//   null,
//   { dragAndDrop }
// )(dropping(Cards));
export default Cards;
