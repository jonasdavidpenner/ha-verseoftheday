/**
 * Bibelvers des Tages - eigene Lovelace-Karte
 *
 * Verwendung:
 *   type: custom:votd-card
 *   entity: sensor.verse_of_the_day
 *   title: Bibelvers des Tages   # optional
 *
 * Die Karte liest den Verstext aus dem Attribut `text` und die Referenz aus
 * dem Attribut `reference` (Fallback: der Sensor-Zustand).
 */

const CARD_VERSION = "1.1.0";

class VotdCard extends HTMLElement {
  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("Du musst eine 'entity' angeben.");
    }
    this._config = config;
    this._built = false;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._built) {
      this._build();
    }
    this._update();
  }

  _build() {
    const card = document.createElement("ha-card");

    const style = document.createElement("style");
    style.textContent = `
      .votd {
        padding: 18px 20px 20px;
      }
      .votd-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 14px;
        color: var(--secondary-text-color);
        font-size: 0.8rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }
      .votd-header ha-icon {
        --mdc-icon-size: 20px;
        color: var(--primary-color);
      }
      .votd-text {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.2rem;
        line-height: 1.6;
        color: var(--primary-text-color);
        border-left: 3px solid var(--primary-color);
        padding-left: 16px;
        white-space: pre-line;
      }
      .votd-reference {
        margin-top: 14px;
        text-align: right;
        font-style: italic;
        color: var(--secondary-text-color);
        font-size: 0.95rem;
      }
      .votd-warn {
        padding: 16px 20px;
        color: var(--error-color, #db4437);
      }
    `;

    const container = document.createElement("div");
    container.className = "votd";
    container.innerHTML = `
      <div class="votd-header">
        <ha-icon icon="mdi:book-cross"></ha-icon>
        <span class="votd-title"></span>
      </div>
      <div class="votd-text"></div>
      <div class="votd-reference"></div>
    `;

    card.appendChild(style);
    card.appendChild(container);
    this.appendChild(card);

    this._card = card;
    this._els = {
      title: container.querySelector(".votd-title"),
      text: container.querySelector(".votd-text"),
      reference: container.querySelector(".votd-reference"),
      container,
    };
    this._built = true;
  }

  _update() {
    const entityId = this._config.entity;
    const stateObj = this._hass.states[entityId];

    if (!stateObj) {
      this._els.container.innerHTML =
        `<div class="votd-warn">Entity <b>${entityId}</b> not found.</div>`;
      return;
    }

    const reference = stateObj.attributes.reference || stateObj.state || "";
    const text = stateObj.attributes.text || "";
    const title =
      this._config.title !== undefined
        ? this._config.title
        : "Verse of the Day";

    // Nur bei Änderung neu schreiben (spart unnötige DOM-Updates).
    if (this._lastText === text && this._lastRef === reference && this._lastTitle === title) {
      return;
    }
    this._lastText = text;
    this._lastRef = reference;
    this._lastTitle = title;

    this._els.title.textContent = title;
    this._els.text.textContent = text || "…";
    this._els.reference.textContent = reference ? `— ${reference}` : "";
  }

  getCardSize() {
    return 3;
  }

  static getStubConfig() {
    return { entity: "sensor.verse_of_the_day" };
  }
}

customElements.define("votd-card", VotdCard);

// Macht die Karte im UI-Karten-Auswahldialog sichtbar.
window.customCards = window.customCards || [];
window.customCards.push({
  type: "votd-card",
  name: "Verse of the Day",
  description: "Shows the daily Bible verse, nicely formatted.",
  preview: true,
});

console.info(
  `%c VOTD-CARD %c v${CARD_VERSION} `,
  "color: white; background: #3f7cac; font-weight: 700;",
  "color: #3f7cac; background: white; font-weight: 700;"
);
